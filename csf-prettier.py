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
    [ "spędzamy zbyt dużo czasu", "przywiązujemy się do starych sposobów", "pomijane są ludzkie aspekty", "nie poświęciliśmy dużo czasu"], 
    [ "osiągnięcie celu", "możliwy przyszły wpływ", "wpływ na innych ludzi", "konsekwencję"],
    [ "w wyniku spóżnionego działania", "wykonałem/am coś, a potem", "wyrządzam innym przykrość", "przeoczyłem/am kilka istotnych faktów"] 
]

c_driver = "Driver"
c_expressive = "Expressive"
c_amiable = "Amiable"
c_analytical = "Analytical"

styles = [ c_driver, c_expressive, c_amiable, c_analytical]

def driver_boost(x, y, value):
    return (x+value,y+value)

def tranform_x(x, style, value):
    if style == c_driver:
        return x+value
    if style == c_expressive:
        return x+value
    if style == c_amiable:
        return x-value
    if style == c_analytical:
        return x-value
    
def tranform_y(y, style, value):
    if style == c_driver:
        return y+value
    if style == c_expressive:
        return y-value
    if style == c_amiable:
        return y-value
    if style == c_analytical:
        return y+value


with open('results3.csv', "r", encoding='utf-8-sig') as csv_file:
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
            print(f'\n{row[0]}')

            for i in range(1,16):
                answer = row[i]
                trait = header[i]
                style = traits_style[trait]
                style_counter[style] += answer_values[answer]

            for key in style_counter:
                print(f'{key}: {style_counter[key]}')

            x_axis_yd = style_counter[c_dominant] - style_counter[c_yield]
            y_axis_ro = style_counter[c_reserved] - style_counter[c_open]
            print(f'Short questions (x,y): {x_axis_yd, y_axis_ro}')


            starting_index = 17
            long_questions_count = 4
            for i in range(starting_index,starting_index + long_questions_count - 1):
                long_answer = row[i].split(";")
                
                questions_num = i - starting_index
                answer_boost = 3
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
                            break

                    answer_boost -= 1

            line_count += 1

            for key in results_values:
                print(f'{key} {results_values[key]}')
                x_axis_yd = tranform_x(x_axis_yd, key, results_values[key])
                y_axis_ro = tranform_y(y_axis_ro, key, results_values[key])

            
            print(f'Short+Long questions (x,y): {x_axis_yd, y_axis_ro}')

    print(f'Processed {line_count} lines.')