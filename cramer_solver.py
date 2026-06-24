def read_size():
    while True:
        raw = input("введите количество неизвестных (2 / 3): ").strip()
        if raw not in ("2", "3"):
            print("ошибка! метод Крамера в этой программе работает только для 2 или 3 неизвестных!")
            continue
        return int(raw)


def read_float(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("ошибка! введите число!")


def read_matrix(n):
    print("\nвведите коэффициенты матрицы по строкам")
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            value = read_float(f"  a[{i + 1}][{j + 1}] = ")
            row.append(value)
        matrix.append(row)
    return matrix


def read_vector(n):
    print("\nвведите свободные члены")
    vector = []
    for i in range(n):
        value = read_float(f"  b[{i + 1}] = ")
        vector.append(value)
    return vector


def determinant(matrix):
    n = len(matrix)

    if n == 1:
        return matrix[0][0]

    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    total = 0.0
    for col in range(n):
        minor = []
        for row in range(1, n):
            minor_row = matrix[row][:col] + matrix[row][col + 1:]
            minor.append(minor_row)
        sign = 1 if col % 2 == 0 else -1
        total += sign * matrix[0][col] * determinant(minor)

    return total


def replace_column(matrix, column_index, new_column):
    n = len(matrix)
    new_matrix = []
    for row in range(n):
        new_row = matrix[row][:]
        new_row[column_index] = new_column[row]
        new_matrix.append(new_row)
    return new_matrix


def cramer_solve(matrix, free_terms):
    main_det = determinant(matrix)

    if abs(main_det) < 1e-12:

        for i in range(len(matrix)):
            modified = replace_column(matrix, i, free_terms)

            if abs(determinant(modified)) > 1e-12:
                return "none", main_det

        return "infinite", main_det

    solution = []

    for i in range(len(matrix)):
        modified = replace_column(matrix, i, free_terms)
        det_i = determinant(modified)
        solution.append(det_i / main_det)

    return solution, main_det


def print_system(matrix, free_terms):
    n = len(matrix)
    print("\nвведённая система уравнений: ")
    for i in range(n):
        terms = []
        for j in range(n):
            terms.append(f"{matrix[i][j]:.1f}*x{j + 1}")
        line = " + ".join(terms)
        print(f"  {line} = {free_terms[i]:.1f}")


def main():
    
    print("Решение СЛУ методом Крамера")
    print("-" * 40)

    n = read_size()
    matrix = read_matrix(n)
    free_terms = read_vector(n)

    print_system(matrix, free_terms)

    solution, main_det = cramer_solve(matrix, free_terms)

    print(f"\nглавный определитель: {main_det:.2f}")

    if solution == "none":
        print("СЛУ не имеет решений (система несовместа)")
        print("Метод Крамера не применим!")
        return

    if solution == "infinite":
        print("СЛУ имеет бесконечно много решений (неопределённая система)")
        print("Метод Крамера не применим!")
        return

    print("\nрешение системы: ")
    for i, value in enumerate(solution):
        print(f"  x{i + 1} = {value:.2f}")


if __name__ == "__main__":
    main()