def baseToDec(input_num:str, base:int):
    if base > 1 and base <= 36:
        if base > 9:
            result = bin(int(input_num, base))
            if result[0] == '-':
                result = result[0] + result[3::]
            else:
                result = result[2::]
            result = baseToDec(result, 2)
        else:
            reversed = input_num[::-1]
            result = 0
            for i in range(len(reversed)):
                n = int(reversed[i])
                result += n * (base**i)
        return result
    return None

def decToBase(input_num:int, base:int):
    if base > 1 and base <= 36:
        numbers_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                        'U', 'V', 'W', 'X', 'Y', 'Z'
                        ]
        result = ''
        while input_num >= base:
            if base > 9:
                result = numbers_list[input_num % base] + result
                input_num = input_num // base

            else:
                result = str(input_num % base) + result
                input_num //= base

        if input_num < base:
            result = str(input_num) + result

        return result
    return None

def baseToBase(input_num:str, input_base:int, output_base:int):
    return decToBase(baseToDec(input_num, input_base), output_base)

if __name__ == "__main__":
    input_num = str(input("Введите числ: "))
    input_base = int(input("Введите основание входного числа: "))
    output_base = int(input("Введите основание выходного числа: "))
    print(baseToBase(input_num, input_base, output_base))