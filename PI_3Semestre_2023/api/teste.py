from ValidaCNPJ import ValidaCNPJ

def main():
    validador = ValidaCNPJ(cnpj='46.362.661/0001-68')
    print_dados = validador.CarregarCNPJ()
    if print_dados is not None:
        print(print_dados)

if __name__ == '__main__':
    main()