import csv

answer_values = {
    "NIE": -4,
    "Raczej NIE": -2,
    "Raczej TAK" : 2,
    "TAK" : 4
}

c_dominant = "Dominant"
c_yield = "Yield"
c_reserved = "Reserved"
c_open = "Open"

traits_style = {
    "Wspierającą" : "Yield",
    "Wymagającą" : "Dominant",
    "Współpracującą" : "Yield",
    "Podejmującą ryzyko" : "Dominant",
    "Pobłażliwą" : "Yield",
    "Zdecydowaną" : "Dominant",
    "Ugodową" : "Yield",
    "Stanowczą" : "Dominant",

    "Rozmowną" : "Open",
    "Poważną" : "Reserved",
    "Spontaniczną" : "Open",
    "Cichą" : "Reserved",
    "Emocjonalną" : "Open",
    "Działającą przemyślanie" : "Reserved",
    "Ciepłą" : "Open",
    "Skrytą" : "Reserved",

    "Otwartą" : "Open", # to remove,
    "Dowcipną" : "Open", # to remove,
    "Rozważną" : "Reserved" # to remove
}
# long_answer_prefixes[0] -> prefixes for first question
# prefixes = long_answer_prefixes[0]
# prefixes[0] -> answer for driver
# prefixes[1] -> answer for expressive
# prefixes[2] -> answer for amiable
# prefixes[3] -> answer for analytical

long_answer_prefixes = [
    [ "wykorzystanie energii", "odkrywanie nowych", "kontakty z innymi", "wykorzystanie logiki"], 
    [ "spędzamy zbyt dużo czasu", "przywiązujemy się do starych sposobów", "pomijane są ludzkie aspekty", "nie poświęciliśmy wystarczająco dużo czasu"], 
    [ "osiągnięcie celu dowolnymi środkami", "możliwy przyszły wpływ", "wpływ na innych ludzi", "konsekwencję, systematyczność"],
    [ "w wyniku spóźnionego działania", "wykonałem/am coś", "wyrządzam innym przykrość", "przeoczyłem/am kilka istotnych faktów"] 
]

c_driver = "Driver"
c_expressive = "Expressive"
c_amiable = "Amiable"
c_analytical = "Analytical"

styles = [ c_driver, c_expressive, c_amiable, c_analytical]

def driver_boost(x, y, value):
    return (x+value,y+value)

def tranform_x(x, style, value):
    value = value/2
    if style == c_driver:
        return x+value
    if style == c_expressive:
        return x+value
    if style == c_amiable:
        return x-value
    if style == c_analytical:
        return x-value
    
def tranform_y(y, style, value):
    value = value/2
    if style == c_driver:
        return y+value
    if style == c_expressive:
        return y-value
    if style == c_amiable:
        return y-value
    if style == c_analytical:
        return y+value


results = {
    c_driver : [],
    c_amiable : [],
    c_expressive : [],
    c_analytical : []
}

def complete(name, style, x, y):
    results[style].append((name, x, y))
    print(f'{style}')

with open('results.csv', "r", encoding='utf-8-sig') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0

    for row in csv_reader:

        style_counter = {
            c_yield : 0,
            c_dominant : 0,
            c_reserved : 0,
            c_open : 0
        }

        results_values = {
            c_driver: 0,
            c_expressive: 0,
            c_amiable : 0,
            c_analytical : 0
        }

        if line_count == 0:
            header = row
            line_count += 1
        else:
            name = row[5]

            print(f'\n{name}')

            for i in range(6,21):
                answer = row[i]
                trait = header[i]
                style = traits_style[trait]
                style_counter[style] += answer_values[answer]

            for key in style_counter:
                print(f'{key}: {style_counter[key]}')

            axis_x = style_counter[c_dominant] - style_counter[c_yield]
            axis_y = style_counter[c_reserved] - style_counter[c_open]
            print(f'Short questions (x,y): {axis_x, axis_y}')


            starting_index = 22
            long_questions_count = 4
            for i in range(starting_index,starting_index + long_questions_count - 1):
                long_answer = row[i].split(";")
                
                questions_num = i - starting_index
                answer_boost = 3
                prefixes_found = []
                for answer in long_answer:
                    prefixes = long_answer_prefixes[questions_num]

                    # prefixes[0] -> answer for driver
                    # prefixes[1] -> answer for expressive
                    # prefixes[2] -> answer for amiable
                    # prefixes[3] -> answer for analytical

                    for prefix in prefixes:
                        if answer.lower().startswith(prefix):
                            style = styles[prefixes.index(prefix)]
                            results_values[style] += answer_boost
                            prefixes_found.append(prefix)
                            break

                    answer_boost -= 1

                if len(prefixes_found) < 4:
                    diff = prefixes.remove(prefixes_found)
                    raise Exception('prefix not found {diff}')
                    
            line_count += 1

            for key in results_values:
                print(f'{key} {results_values[key]}')
                axis_x = tranform_x(axis_x, key, results_values[key])
                axis_y = tranform_y(axis_y, key, results_values[key])

            print(f'Short+Long questions (x,y): {axis_x, axis_y}')

            style = 'none'

            if axis_x > 0 and axis_y > 0:
                style = c_driver

            if axis_x > 0 and axis_y < 0:
                style = c_expressive

            if axis_x <= 0 and axis_y >= 0:
                style = c_analytical

            if axis_x <= 0 and axis_y <= 0:
                style = c_amiable

            if style == 'none':
                raise Exception(f'style {axis_x},{axis_y} for {row[5]}')

            complete(name, style, axis_x, axis_y)

    def to_json(p):
        return f'{{ x: {p[1]}, y: {p[2]} }}'

    def to_csv_with_name(p):
        return f'{p[0]};{p[1]};{p[2]}'

    for key in results:
        print(f'\n{key} {len(results[key])}')
        points = map(to_json, results[key])
        text = ',\n'.join(points);
        print(f'{text}')

    for key in results:
        print(f'\n{key} {len(results[key])}')
        points = map(to_csv_with_name, results[key])
        text = ',\n'.join(points)
        print(f'{text}')


    print(f'\n')
    print(f'\tProcessed {line_count} lines.')