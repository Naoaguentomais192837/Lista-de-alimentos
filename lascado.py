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
    estado_edicao = {"id": None}  
    def mostrar_pagina_registro(dados=None):
        page.clean()
        titulo = ft.Text(value='Novo Registro', size=30)

        entrada_alimento = ft.TextField(label='Alimento')
        entrada_caloria = ft.TextField(label='Calorias (KCAL)', keyboard_type=ft.KeyboardType.NUMBER)
        entrada_proteina = ft.TextField(label='Proteínas (g)', keyboard_type=ft.KeyboardType.NUMBER)
        entrada_carboidrato = ft.TextField(label='Carboidratos (g)', keyboard_type=ft.KeyboardType.NUMBER)
        entrada_gorduras = ft.TextField(label='Gorduras (g)', keyboard_type=ft.KeyboardType.NUMBER)
        entrada_gordurasTrans = ft.TextField(label='Gorduras Trans (g)', keyboard_type=ft.KeyboardType.NUMBER)

        if dados:
            estado_edicao["id"] = dados["id"]
            entrada_alimento.value = dados["alimento"]
            entrada_caloria.value = str(dados["caloria"])
            entrada_proteina.value = str(dados["proteina"])
            entrada_carboidrato.value = str(dados["carboidrato"])
            entrada_gorduras.value = str(dados["gordura"])
            entrada_gordurasTrans.value = str(dados["gordura_trans"])

        def salvar_registro(e):
            try:
                alimento = entrada_alimento.value.strip()
                caloria = float(entrada_caloria.value)
                proteina = float(entrada_proteina.value)
                carboidrato = float(entrada_carboidrato.value)
                gordura = float(entrada_gorduras.value)
                gordura_trans = float(entrada_gordurasTrans.value)

                with conectar_bd() as conn:
                    cursor = conn.cursor()
                    if estado_edicao["id"] is None:
                        cursor.execute(
                            "INSERT INTO alimentos (alimento, caloria, proteina, carboidrato, gordura, gordura_trans) VALUES (?, ?, ?, ?, ?, ?)",
                            (alimento, caloria, proteina, carboidrato, gordura, gordura_trans)
                        )
                    else:
                        cursor.execute(
                            "UPDATE alimentos SET alimento=?, caloria=?, proteina=?, carboidrato=?, gordura=?, gordura_trans=? WHERE id=?",
                            (alimento, caloria, proteina, carboidrato, gordura, gordura_trans, estado_edicao["id"])
                        )
                        estado_edicao["id"] = None
                    conn.commit()
                mostrar_pagina_lista()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao salvar: {ex}"), open=True)
                page.update()

        page.add(
            titulo,
            entrada_alimento,
            entrada_caloria,
            entrada_proteina,
            entrada_carboidrato,
            entrada_gorduras,
            entrada_gordurasTrans,
            ft.Row([
                ft.ElevatedButton('Salvar', on_click=salvar_registro),
                ft.ElevatedButton("Ver Lista", on_click=lambda e: mostrar_pagina_lista())
            ])
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
                def editar_item(e, id=item_id, a=alimento, c=cal, p=prot, ca=carb, g=gord, gt=gord_trans):
                    mostrar_pagina_registro({
                        "id": id,
                        "alimento": a,
                        "caloria": c,
                        "proteina": p,
                        "carboidrato": ca,
                        "gordura": g,
                        "gordura_trans": gt
                    })

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

        page.add(
            titulo,
            campo_busca,
            ft.Container(content=tabela_dados, width=page.width, alignment=ft.alignment.center, padding=20),
            ft.Row([
                ft.ElevatedButton("Adicionar Novo Alimento", on_click=lambda e: mostrar_pagina_registro())
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
        atualizar_tabela()

    mostrar_pagina_lista()

ft.app(target=main)
