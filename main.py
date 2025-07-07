import flet as ft

def main(page: ft.Page):
    registro = ft.Text(value='Registro', size=30)
    page.controls.append(registro)
    page.update()

    # página de registro

    def registro(e):
        #mensagens de erros
        if not entrada_alimento.value:
            entrada_alimento.error_text = 'Por favor preencha corretamente'
            page.uptade()
        if not entrada_caloria.value:
            entrada_caloria.error_text = 'Por favor preencha corretamente'
            page.uptade()
        if not entrada_proteina.value:
            entrada_proteina.error_text = 'Por favor preencha corretamente'
            page.uptade()
        if not entrada_carboidrato.value:
            entrada_carboidrato.error_text = 'Por favor preencha corretamente'
            page.uptade()
        if not entrada_gorduras.value:
            entrada_gorduras.error_text = 'Por favor preencha corretamente'
            page.uptade()
        if not entrada_gordurasTrans.value:
            entrada_gordurasTrans.error_text = 'Por favor preencha corretamente'
            page.uptade()

        else:
            alimento = entrada_alimento.value
            caloria = entrada_caloria.value
            proteina = entrada_proteina.value
            carboidratos = entrada_carboidrato.value
            gorduras = entrada_gorduras.value
            gordurasTrans = entrada_gordurasTrans.value

            print(f"Alimento: {alimento}\nCaloria: {caloria}\nProteina: {proteina}\nCarboidratos {carboidratos}\nGorduras: {gorduras}\nGorduras Trans: {gordurasTrans}")

            page.clean()
            page.add(ft.Text('Lista'))

    #Campos de entrada
    entrada_alimento = ft.TextField(label='alimento')
    entrada_caloria = ft.TextField(label='calorias KCAL')
    entrada_proteina = ft.TextField(label='proteinas')
    entrada_carboidrato = ft.TextField(label='carboidratos')
    entrada_gorduras = ft.TextField(label='gorduras')
    entrada_gordurasTrans = ft.TextField(label='gorduras Transgênicas')

    #Adiciona os campos à página
    page.add(
        entrada_alimento,
        entrada_caloria,
        entrada_proteina,
        entrada_carboidrato,
        entrada_gorduras,
        entrada_gordurasTrans,
        ft.ElevatedButton('Salvar', on_click=registro)
    )

ft.app(target=main)