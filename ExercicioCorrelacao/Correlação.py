import math

tempo_estudo = [2, 4, 5, 6, 8]

nota_final = [60, 70, 75, 78, 85]


def media():
    media_x = sum(tempo_estudo) / len(tempo_estudo)
    media_y = sum(nota_final) / len(nota_final)

    return media_x, media_y


def covariancia():
    cov_result = []

    for i in range(len(tempo_estudo)):
        # (xi - xm)
        x = tempo_estudo[i] - media()[0]

        # (yi - ym)
        y = nota_final[i] - media()[1]

        cov_result.append(x * y)

    return sum(cov_result) / len(tempo_estudo)


def desvio_padrao():
    x = []
    y = []
    for i in range(len(tempo_estudo)):
        desvio_x = (tempo_estudo[i] - media()[0]) ** 2

        x.append(desvio_x)

        desvio_y = (nota_final[i] - media()[1]) ** 2

        y.append(desvio_y)

    resultado_x = math.sqrt(sum(x) / len(tempo_estudo))
    resultado_y = math.sqrt(sum(y) / len(nota_final))

    return resultado_x, resultado_y


def correlacao_person():
    correlacao = covariancia() / (desvio_padrao()[0] * desvio_padrao()[1])

    return correlacao


if correlacao_person() < 0:
    print(f'{correlacao_person()} é negativa ou seja os dados caminham em direção contraria.. ')

elif abs(correlacao_person()) < 1e-5:
    print(f'{correlacao_person()} muito próximo de zero isso tende a ser uma relação nula ')

else:
    print(f'{correlacao_person()} isso significa que a relação é linear. ')
