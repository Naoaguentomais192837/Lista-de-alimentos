import flet as ft
import sqlite3

def conectar_bd():
    conn = sqlite3.connect('nutricao.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alimento TEXT NOT NULL,
            caloria REAL NOT NULL,
            proteina REAL NOT NULL,
            carboidrato REAL NOT NULL,
            gordura REAL NOT NULL,
            gordura_trans REAL NOT NULL
        )
    ''')
    conn.commit()
    return conn

def main(page: ft.Page):
    page.title = "Controle Nutricional"

    def mostrar_pagina_registro():
        page.clean()
        titulo = ft.Text(value='Registro de Alimento', size=30)

        entrada_alimento = ft.TextField(label='Alimento')
        entrada_caloria = ft.TextField(label='Calorias (KCAL)', keyboard_type=ft.KeyboardType.NUMBER)
        entrada_proteina = ft.TextField(label='Proteínas (g)', keyboard_type=ft.KeyboardType.NUMBER)
        entrada_carboidrato = ft.TextField(label='Carboidratos (g)', keyboard_type=ft.KeyboardType.NUMBER)
        entrada_gorduras = ft.TextField(label='Gorduras (g)', keyboard_type=ft.KeyboardType.NUMBER)
        entrada_gordurasTrans = ft.TextField(label='Gorduras Trans (g)', keyboard_type=ft.KeyboardType.NUMBER)

        def limpar_campos():
            entrada_alimento.value = ""
            entrada_caloria.value = ""
            entrada_proteina.value = ""
            entrada_carboidrato.value = ""
            entrada_gorduras.value = ""
            entrada_gordurasTrans.value = ""

        def salvar_registro(e):
            erros = False
            if not entrada_alimento.value.strip():
                entrada_alimento.error_text = 'Campo obrigatório'
                erros = True
            if not entrada_caloria.value:
                entrada_caloria.error_text = 'Campo obrigatório'
                erros = True
            if not entrada_proteina.value:
                entrada_proteina.error_text = 'Campo obrigatório'
                erros = True
            if not entrada_carboidrato.value:
                entrada_carboidrato.error_text = 'Campo obrigatório'
                erros = True
            if not entrada_gorduras.value:
                entrada_gorduras.error_text = 'Campo obrigatório'
                erros = True
            if not entrada_gordurasTrans.value:
                entrada_gordurasTrans.error_text = 'Campo obrigatório'
                erros = True

            if erros:
                page.update()
                return

            try:
                with conectar_bd() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO alimentos (alimento, caloria, proteina, carboidrato, gordura, gordura_trans) VALUES (?, ?, ?, ?, ?, ?)",
                        (
                            entrada_alimento.value.strip(),
                            float(entrada_caloria.value),
                            float(entrada_proteina.value),
                            float(entrada_carboidrato.value),
                            float(entrada_gorduras.value),
                            float(entrada_gordurasTrans.value),
                        ),
                    )
                    conn.commit()
                limpar_campos()
                mostrar_pagina_lista()
            except ValueError:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Por favor, insira valores numéricos válidos."),
                    open=True,
                )
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Erro ao salvar dados: {ex}"),
                    open=True,
                )
                page.update()

        page.add(
            titulo,
            entrada_alimento,
            entrada_caloria,
            entrada_proteina,
            entrada_carboidrato,
            entrada_gorduras,
            entrada_gordurasTrans,
            ft.ElevatedButton('Salvar', on_click=salvar_registro),
            ft.ElevatedButton("Ver Lista", on_click=lambda e: mostrar_pagina_lista())
        )
        page.update()

    def mostrar_pagina_lista():
        page.clean()
        titulo = ft.Text("Alimentos Registrados", size=30)
        campo_busca = ft.TextField(label="Buscar alimento", on_change=lambda e: atualizar_tabela(campo_busca.value))
        tabela_dados = ft.DataTable(columns=[
            ft.DataColumn(ft.Text("Alimento")),
            ft.DataColumn(ft.Text("Calorias")),
            ft.DataColumn(ft.Text("Proteínas")),
            ft.DataColumn(ft.Text("Carboidratos")),
            ft.DataColumn(ft.Text("Gorduras")),
            ft.DataColumn(ft.Text("Gord. Trans")),
            ft.DataColumn(ft.Text("Ações")),
        ], rows=[])

        def atualizar_tabela(query_busca=""):
            with conectar_bd() as conn:
                cursor = conn.cursor()
                sql = "SELECT id, alimento, caloria, proteina, carboidrato, gordura, gordura_trans FROM alimentos"
                params = []
                if query_busca.strip():
                    sql += " WHERE alimento LIKE ?"
                    params.append(f"%{query_busca.strip()}%")
                cursor.execute(sql, params)
                dados = cursor.fetchall()

            tabela_dados.rows.clear()
            for item_id, alimento, cal, prot, carb, gord, gord_trans in dados:
                def editar_item(e, id=item_id):
                    abrir_dialogo_edicao(id, alimento, cal, prot, carb, gord, gord_trans)

                def excluir_item(e, id=item_id):
                    with conectar_bd() as conn:
                        conn.execute("DELETE FROM alimentos WHERE id = ?", (id,))
                        conn.commit()
                    atualizar_tabela(campo_busca.value)
                    page.snack_bar = ft.SnackBar(ft.Text("Item excluído com sucesso!"), open=True)
                    page.update()

                tabela_dados.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(alimento)),
                        ft.DataCell(ft.Text(str(cal))),
                        ft.DataCell(ft.Text(str(prot))),
                        ft.DataCell(ft.Text(str(carb))),
                        ft.DataCell(ft.Text(str(gord))),
                        ft.DataCell(ft.Text(str(gord_trans))),
                        ft.DataCell(ft.Row([
                            ft.IconButton(icon=ft.icons.EDIT, on_click=editar_item),
                            ft.IconButton(icon=ft.icons.DELETE, on_click=excluir_item, icon_color=ft.colors.RED_500),
                        ])),
                    ])
                )
            page.update()

        def abrir_dialogo_edicao(id, a, c, p, ca, g, gt):
            f1 = ft.TextField(label='Alimento', value=a)
            f2 = ft.TextField(label='Calorias', value=str(c), keyboard_type=ft.KeyboardType.NUMBER)
            f3 = ft.TextField(label='Proteínas', value=str(p), keyboard_type=ft.KeyboardType.NUMBER)
            f4 = ft.TextField(label='Carboidratos', value=str(ca), keyboard_type=ft.KeyboardType.NUMBER)
            f5 = ft.TextField(label='Gorduras', value=str(g), keyboard_type=ft.KeyboardType.NUMBER)
            f6 = ft.TextField(label='Gorduras Trans', value=str(gt), keyboard_type=ft.KeyboardType.NUMBER)

            def salvar_edicao(e):
                try:
                    with conectar_bd() as conn:
                        conn.execute(
                            "UPDATE alimentos SET alimento=?, caloria=?, proteina=?, carboidrato=?, gordura=?, gordura_trans=? WHERE id=?",
                            (
                                f1.value.strip(),
                                float(f2.value),
                                float(f3.value),
                                float(f4.value),
                                float(f5.value),
                                float(f6.value),
                                id,
                            )
                        )
                        conn.commit()
                    dialogo.open = False
                    atualizar_tabela(campo_busca.value)
                    page.snack_bar = ft.SnackBar(ft.Text("Item atualizado com sucesso!"), open=True)
                    page.update()
                except Exception as ex:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao editar: {ex}"), open=True)
                    page.update()

            dialogo = ft.AlertDialog(
                modal=True,
                title=ft.Text("Editar Alimento"),
                content=ft.Column([f1, f2, f3, f4, f5, f6], tight=True),
                actions=[
                    ft.TextButton("Salvar", on_click=salvar_edicao),
                    ft.TextButton("Cancelar", on_click=lambda e: fechar_dialogo(dialogo)),
                ],
            )
            page.dialog = dialogo
            dialogo.open = True
            page.update()

        def fechar_dialogo(dlg):
            dlg.open = False
            page.update()

        page.add(
            titulo,
            campo_busca,
            ft.Container(content=tabela_dados, width=page.width, alignment=ft.alignment.center, padding=20),
            ft.ElevatedButton("Adicionar Novo Alimento", on_click=lambda e: mostrar_pagina_registro())
        )
        atualizar_tabela()

    mostrar_pagina_registro()

ft.app(target=main)