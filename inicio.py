import flet as ft

# Lista global para armazenar os registros
registros = []

def main(page: ft.Page):
    page.title = "Registro"

    def mostrar_lista():
        # Limpa a página e exibe os dados salvos em formato de tabela horizontal
        page.clean()
        page.add(ft.Text("Lista de Alimentos Registrados", size=30))

        #Cria tabela com colunas fixas (horizontal)
        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Alimento")),
                ft.DataColumn(ft.Text("Calorias")),
                ft.DataColumn(ft.Text("Proteínas")),
                ft.DataColumn(ft.Text("Carboidratos")),
                ft.DataColumn(ft.Text("Gorduras")),
                ft.DataColumn(ft.Text("Gord. Trangênicas")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(reg["alimento"])),
                        ft.DataCell(ft.Text(reg["calorias"])),
                        ft.DataCell(ft.Text(reg["proteinas"])),
                        ft.DataCell(ft.Text(reg["carboidratos"])),
                        ft.DataCell(ft.Text(reg["gorduras"])),
                        ft.DataCell(ft.Text(reg["gorduras_trans"]))
                    ]
                ) for reg in registros
            ]
        )

        page.add(
            tabela,
            ft.ElevatedButton("Voltar ao Registro", on_click=lambda e: mostrar_registros())
        )
        page.update()

    def mostrar_registros(e=None):
        page.clean()
        page.add(ft.Text(value='Registro', size=30))

        # Campos de entrada
        entrada_alimento = ft.TextField(label='Alimento')
        entrada_caloria = ft.TextField(label='Calorias (KCAL)')
        entrada_proteina = ft.TextField(label='Proteínas')
        entrada_carboidrato = ft.TextField(label='Carboidratos')
        entrada_gorduras = ft.TextField(label='Gorduras')
        entrada_gordurasTrans = ft.TextField(label='Gorduras Transgênicas')

        def registro(e):
            campos = [
                ("alimento", entrada_alimento),
                ("calorias", entrada_caloria),
                ("proteinas", entrada_proteina),
                ("carboidratos", entrada_carboidrato),
                ("gorduras", entrada_gorduras),
                ("gorduras_trans", entrada_gordurasTrans),
            ]

            # Limpe mensagens de erro 
            for _, campo in campos:
                campo.error_text = None
            
            # Verifica se há campo vazio
            if any(not campo.value for _, campo in campos):
                for _, campo in campos:
                    if not campo.value:
                        campo.error_text = 'Por favor preencha corretamente'
                page.update()
                return
            
            # Salva o registro completo como um dicionário
            novo_registro = {nome: campo.value for nome, campo in campos}
            registros.append(novo_registro)

            # Limpa os campos após salvar
            for _, campo in campos:
                campo.value = ""

            page.update()

        # Adiciona os campos e botões à página
        page.add(
            entrada_alimento,
            entrada_caloria,
            entrada_proteina,
            entrada_carboidrato,
            entrada_gorduras,
            entrada_gordurasTrans,
            ft.ElevatedButton('Salvar', on_click=registro),
            ft.ElevatedButton("Ver Lista", on_click=lambda e: mostrar_lista())
        )

        page.uptade()