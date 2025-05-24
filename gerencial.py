######################################################## 
# Faculdade: Cesar School                              #
# Curso: Segurança da Informação                       #
# Período: 2025.1                                      #
# Disciplina: Projeto 1                                #
# Professor de Projeto 1: Humberto Caetano             #
# Professora de Fundamentos de Programação: Carol Melo #
# Projeto: App Denúncia de Bullying Anônima            #
# Descrição: Módulo Gerencial                          #
# Equipe:                                              #
#           Artur Cavalcanti                           #
#           Eduardo Henrique Ferreira Fonseca Barbosa  #
#           Evandro José Rodrigues Torres Zacarias     #
#           Gabriel de Medeiros Almeida                #
#           Maria Clara Miranda                        #
#           Mauro Sérgio Rezende da Silva              #
#           Silvio Barros Tenório                      #
# Versão: 1.6                                          #
# Data: 24/05/2025                                     #
######################################################## 

import dados
import utilidades
import flet as ft
import re
import webbrowser
from pathlib import Path
from datetime import datetime
import asyncio

# Constantes
BANCO_DADOS = "bullying.db"
CAMINHO_BANCO_DADOS = Path(BANCO_DADOS)
FORMATO_DATA = "%d/%m/%Y"
FORMATO_DATA_HORA = "%d/%m/%Y %H:%M:%S"
FORMATO_DATA_HORA_ISO = "%Y-%m-%d %H:%M:%S.%f"

# Variáveis Globais
usuario_autenticado = False
usuario_id = 0
usuario_nome = ""
usuario_tipo = ""
usuario_email = ""
denuncia_id = 0
denuncia_id_gerado = 0
data_reuniao = datetime.now().date()
flag_thread = False
flag_atualiza = False
reniao_id = 0
status = ""
w_usuario_id = 0
w_material_id = 0

# Função de Início da Aplicação
def main(page: ft.Page):
    try:
        # Instância do Banco de Dados
        bd = dados.BancoDados(BANCO_DADOS)
        print("[Banco de Dados Instânciado]")

        # Verifica se o Banco de Dados existe, se não cria as tabelas.
        if not (CAMINHO_BANCO_DADOS.exists()):
            print("[Criar Tabelas]")
            bd.criar_tabelas()

        # Título do App
        page.title = "Denúncia de Bullying Anônima - Módulo Gerencial  [V.1.6]"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20

        # Evento de mudança de view
        def route_change(e):
            global usuario_autenticado
            global usuario_id
            global usuario_nome
            global usuario_tipo
            global usuario_email
            global denuncia_id
            global denuncia
            global denuncia_id_gerado
            global data_reuniao
            global flag_thread
            global flag_atualiza
            global reuniao_id
            global lv_reuniao
            global status
            global w_usuario_id
            global w_material_id
            global button_style

            button_style = ft.ButtonStyle(
                color={
                    ft.ControlState.DEFAULT: ft.Colors.BLACK,
                    ft.ControlState.DISABLED: ft.Colors.with_opacity(0.38, ft.Colors.BLACK),
                    ft.ControlState.HOVERED: ft.Colors.BLACK,
                    ft.ControlState.PRESSED: ft.Colors.BLACK,
                },
                icon_color={
                    ft.ControlState.DEFAULT: ft.Colors.BLACK,
                    ft.ControlState.DISABLED: ft.Colors.with_opacity(0.38, ft.Colors.BLACK),
                    ft.ControlState.HOVERED: ft.Colors.BLACK,
                    ft.ControlState.PRESSED: ft.Colors.BLACK,
                },
                bgcolor={
                    ft.ControlState.DEFAULT: "#5FBF60",
                    ft.ControlState.DISABLED: ft.Colors.with_opacity(0.12, "#D4F1C1"),
                    ft.ControlState.HOVERED: ft.Colors.with_opacity(0.8, "#5FBF60"),
                    ft.ControlState.PRESSED: ft.Colors.with_opacity(0.5, "#5FBF60"),
                },
                overlay_color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(1, ft.Colors.BLACK),
                    ft.ControlState.DISABLED: ft.BorderSide(1, ft.Colors.with_opacity(0.38, ft.Colors.BLACK)),
                    ft.ControlState.HOVERED: ft.BorderSide(2, ft.Colors.BLACK),
                    ft.ControlState.PRESSED: ft.BorderSide(5, ft.Colors.BLACK),
                },
                elevation={
                    ft.ControlState.DEFAULT: 0,
                    ft.ControlState.HOVERED: 0,
                    ft.ControlState.PRESSED: 0,
                },
                # shape=ft.RoundedRectangleBorder(radius=15),
                shape=ft.StadiumBorder(),
                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                animation_duration=200,
            )

            page.views.clear()

            # Validar Email
            def validar_email(e):
                nonlocal email_valida
                email_valida = False
                lb_erro.value = ""
                # Verifica email
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', tf_email.value):  # type: ignore
                    tf_email.error_text = "Email inválido"
                else:
                    tf_email.error_text = ""
                    email_valida = True
                validar_login()   
                page.update()

            # Validar Senha
            def validar_senha(e):
                nonlocal senha_valida
                senha_valida = True
                validar_login()   
                page.update()

            # Validar Senha Atual
            def validar_senha_atual(e):
                nonlocal senha_atual_valida
                senha_atual_valida = True
                validar_mudar_senha()   
                page.update()

            # Validar Senha Nova
            def validar_senha_nova(e):
                nonlocal senha_nova_valida
                senha_nova_valida = False
                senha_nova = tf_senha_nova.value
                erros = []
                # Verifica cada requisito individualmente
                if len(senha_nova) < 8: # type: ignore 
                    erros.append("Mínimo 8 caracteres")
                if not re.search(r'[A-Z]', senha_nova): # type: ignore
                    erros.append("Pelo menos 1 letra maiúscula")
                if not re.search(r'[a-z]', senha_nova): # type: ignore
                    erros.append("Pelo menos 1 letra minúscula")
                if not re.search(r'[0-9]', senha_nova): # type: ignore
                    erros.append("Pelo menos 1 número")
                if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha_nova): # type: ignore
                    erros.append("Pelo menos 1 símbolo especial")

                if erros:
                    tf_senha_nova.error_text = "\n".join(erros)
                    # Exibe quais requisitos foram atendidos
                    cl_validacao_indicadores.controls = [
                        ft.Row([
                            ft.Text("A senha deve conter", color="grey")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if len(senha_nova) >= 8 else ft.Icons.CLOSE, # type: ignore
                            color="green" if len(senha_nova) >= 8 else "red"), # type: ignore
                            ft.Text("8+ caracteres")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if re.search(r'[A-Z]', senha_nova) else ft.Icons.CLOSE, # type: ignore
                            color="green" if re.search(r'[A-Z]', senha_nova) else "red"), # type: ignore
                            ft.Text("Letra maiúscula")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if re.search(r'[a-z]', senha_nova) else ft.Icons.CLOSE, # type: ignore
                                color="green" if re.search(r'[a-z]', senha_nova) else "red"), # type: ignore
                            ft.Text("Letra minúscula")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if re.search(r'[0-9]', senha_nova) else ft.Icons.CLOSE, # type: ignore
                                color="green" if re.search(r'[0-9]', senha_nova) else "red"), # type: ignore
                            ft.Text("Número")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if re.search(r'[!@#$%^&*(),.?":{}|<>]', senha_nova) else ft.Icons.CLOSE, # type: ignore
                                color="green" if re.search(r'[!@#$%^&*(),.?":{}|<>]', senha_nova) else "red"), # type: ignore
                            ft.Text("Símbolo especial")
                        ])
                    ]
                else:
                    tf_senha_nova.error_text = None
                    senha_nova_valida = True
                    cl_validacao_indicadores.controls = [
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color="green"),
                            ft.Text("Senha forte!", weight=ft.FontWeight.BOLD)
                        ]),
                    ]
        
                cl_validacao_indicadores.update()
                validar_mudar_senha()
                page.update()
                validar_senha_nova_confirmar(e)

            # Validar Senha Nova Confirmar
            def validar_senha_nova_confirmar(e):
                nonlocal senha_nova_confirmar_valida
                senha_nova_confirmar_valida = False
                senha_nova = tf_senha_nova.value
                senha_nova_confirmar = tf_senha_nova_confirmar.value
                errosc = []
                # Verifica cada requisito individualmente
                if len(senha_nova_confirmar) < 8: # type: ignore 
                    errosc.append("Mínimo 8 caracteres")
                if not re.search(r'[A-Z]', senha_nova_confirmar): # type: ignore
                    errosc.append("Pelo menos 1 letra maiúscula")
                if not re.search(r'[a-z]', senha_nova_confirmar): # type: ignore
                    errosc.append("Pelo menos 1 letra minúscula")
                if not re.search(r'[0-9]', senha_nova_confirmar): # type: ignore
                    errosc.append("Pelo menos 1 número")
                if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha_nova_confirmar): # type: ignore
                    errosc.append("Pelo menos 1 símbolo especial")
                if not senha_nova == senha_nova_confirmar:
                    errosc.append("Confirma Senha")

                if errosc:
                    tf_senha_nova_confirmar.error_text = "\n".join(errosc)
                    # Exibe quais requisitos foram atendidos
                    cl_validacao_indicadores_confirmar.controls = [
                        ft.Row([
                            ft.Text("A senha deve conter", color="grey")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if len(senha_nova_confirmar) >= 8 else ft.Icons.CLOSE, # type: ignore
                            color="green" if len(senha_nova_confirmar) >= 8 else "red"), # type: ignore
                            ft.Text("8+ caracteres")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if re.search(r'[A-Z]', senha_nova_confirmar) else ft.Icons.CLOSE, # type: ignore
                            color="green" if re.search(r'[A-Z]', senha_nova_confirmar) else "red"), # type: ignore
                            ft.Text("Letra maiúscula")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if re.search(r'[a-z]', senha_nova_confirmar) else ft.Icons.CLOSE, # type: ignore
                                color="green" if re.search(r'[a-z]', senha_nova_confirmar) else "red"), # type: ignore
                            ft.Text("Letra minúscula")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if re.search(r'[0-9]', senha_nova_confirmar) else ft.Icons.CLOSE, # type: ignore
                                color="green" if re.search(r'[0-9]', senha_nova_confirmar) else "red"), # type: ignore
                            ft.Text("Número")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if re.search(r'[!@#$%^&*(),.?":{}|<>]', senha_nova_confirmar) else ft.Icons.CLOSE, # type: ignore
                                color="green" if re.search(r'[!@#$%^&*(),.?":{}|<>]', senha_nova_confirmar) else "red"), # type: ignore
                            ft.Text("Símbolo especial")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if senha_nova_confirmar == senha_nova else ft.Icons.CLOSE,
                                color="green" if senha_nova_confirmar == senha_nova else "red"),
                            ft.Text("Confirma Senha")
                        ])
                    ]
                else:
                    tf_senha_nova_confirmar.error_text = None
                    senha_nova_confirmar_valida = True
                    cl_validacao_indicadores_confirmar.controls = [
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color="green"),
                            ft.Text("Senha Confirmada!", weight=ft.FontWeight.BOLD)
                        ]),
                    ]
        
                cl_validacao_indicadores_confirmar.update()
                validar_mudar_senha()
                page.update()

            # Validar Email Usuário
            def validar_email_usuario(e):
                nonlocal email_usuario_valida
                email_usuario_valida = False
                lb_erro_usuario.value = ""
                # Verifica email
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', tf_email_usuario.value):  # type: ignore
                    tf_email_usuario.error_text = "Email inválido"
                else:
                    tf_email_usuario.error_text = ""
                    email_usuario_valida = True
                validar_usuario()   
                page.update()

            # Validar Nome Usuário
            def validar_nome_usuario(e):
                nonlocal nome_usuario_valida
                nome_usuario_valida = False
                if not tf_nome_usuario.value.strip():  # type: ignore
                    tf_nome_usuario.error_text = "Requer preenchimento"
                else:
                    tf_nome_usuario.error_text = None
                    nome_usuario_valida = True
                validar_usuario()   
                page.update()

            # Validar Tipo Usuário
            def validar_tipo_usuario(e):
                nonlocal tipo_usuario_valida
                tipo_usuario_valida = False
                if not dd_tipo_usuario.value.strip():  # type: ignore
                    dd_tipo_usuario.error_text = "Requer preenchimento"
                else:
                    dd_tipo_usuario.error_text = None
                    tipo_usuario_valida = True
                validar_usuario()   
                page.update()

            # Validar Usuario
            def validar_usuario():
                nonlocal email_usuario_valida
                nonlocal nome_usuario_valida
                nonlocal tipo_usuario_valida
                usuario_validado = all([
                    email_usuario_valida,
                    nome_usuario_valida,
                    tipo_usuario_valida
                ])
                bt_criar_usuario.disabled = not usuario_validado

            # Validar login
            def validar_login():
                nonlocal email_valida
                nonlocal senha_valida
                login_validado = all([
                    email_valida,
                    senha_valida
                ])
                bt_login.disabled = not login_validado

            # Seleciona Denúncia
            def seleciona_denuncia(e, select_denuncia):
                global denuncia_id
                denuncia_id = select_denuncia
                return page.go("/acompanhar")

            # Validar Mudar Senha
            def validar_mudar_senha():
                nonlocal senha_atual_valida
                nonlocal senha_nova_valida
                nonlocal senha_nova_confirmar_valida
                mudar_senha_validado = all([
                    senha_atual_valida,
                    senha_nova_valida,
                    senha_nova_confirmar_valida
                ])
                bt_mudar_senha.disabled = not mudar_senha_validado

            # Validar Nome Usuário Edição
            def validar_nome_usuario_e(e):
                nonlocal nome_usuario_valida
                nome_usuario_valida = True
                if not tf_nome_usuario.value.strip():  # type: ignore
                    tf_nome_usuario.error_text = "Requer preenchimento"
                    nome_usuario_valida = False
                else:
                    tf_nome_usuario.error_text = None
                    nome_usuario_valida = True
                validar_usuario_e()   
                page.update()

            # Validar Tipo Usuário Edição
            def validar_tipo_usuario_e(e):
                nonlocal tipo_usuario_valida
                tipo_usuario_valida = True
                if not dd_tipo_usuario.value.strip():  # type: ignore
                    dd_tipo_usuario.error_text = "Requer preenchimento"
                    tipo_usuario_valida = False
                else:
                    dd_tipo_usuario.error_text = None
                    tipo_usuario_valida = True
                validar_usuario_e()   
                page.update()

            # Validar Status Usuário Edição
            def validar_status_usuario_e(e):
                nonlocal status_usuario_valida
                status_usuario_valida = True
                if not dd_status_usuario.value.strip():  # type: ignore
                    dd_status_usuario.error_text = "Requer preenchimento"
                    status_usuario_valida = False
                else:
                    dd_status_usuario.error_text = None
                    status_usuario_valida = True
                validar_usuario_e()   
                page.update()

            # Validar Usuario Edição
            def validar_usuario_e():
                nonlocal nome_usuario_valida
                nonlocal tipo_usuario_valida
                nonlocal status_usuario_valida
                usuario_validado = all([
                    nome_usuario_valida,
                    tipo_usuario_valida,
                    status_usuario_valida
                ])
                bt_editar_usuario.disabled = not usuario_validado

            # Login
            def login(e):
                global usuario_autenticado
                global usuario_id
                global usuario_nome
                global usuario_tipo
                global usuario_email
                usuario = bd.verificar_login_usuario(email=tf_email.value) # type: ignore
                if usuario == None:
                    lb_erro.value = "Login inválido"
                    page.update()
                    return None
                else:
                    if utilidades.verificar_hash_bcrypt(tf_senha.value, usuario["Senha"]): # type: ignore
                       usuario_autenticado = True
                       usuario_id = usuario["UsuarioId"]
                       usuario_nome = usuario["Nome"]
                       usuario_tipo = usuario["Tipo"]
                       usuario_email = usuario["Email"]
                       return page.go("/menu")
                    else:
                       lb_erro.value = "Login inválido [Autenticação]"
                       page.update()
                       return None

            # Validar Comentário
            def validar_comentario(e):
                nonlocal comentario_valida
                comentario_valida = False
                comentario = tf_comentario.value
                erros = []
                # Verifica cada requisito individualmente
                if comentario:
                    if len(comentario) < 1:
                        erros.append("Mínimo 1 caractere")
                else:
                    erros.append("Comentário requerido")
                if erros:
                   comentario_valida = False
                   tf_comentario.error_text = "Comentario inválido"
                else:
                   comentario_valida = True
                   tf_comentario.error_text = None
                validar_envio_comentario()   
                page.update()

            # Validar Status
            def validar_status(e):
                nonlocal status_valida
                status_valida = False
                if not dd_status.value.strip():  # type: ignore
                    dd_status_error_text = "Requer preenchimento"
                else:
                    dd_status.error_text = None
                    status_valida = True
                validar_envio_comentario()   
                page.update()

            # Validar Envio Comentário
            def validar_envio_comentario():
                nonlocal comentario_valida
                nonlocal status_valida
                comentario_validado = all([
                    comentario_valida,
                    status_valida
                ])
                bt_salvar_comentario.disabled = not comentario_validado

            # Validar Descrição Material Educativo
            def validar_descricao_material(e):
                nonlocal descricao_material_valida
                descricao_material_valida = False
                if not tf_descricao_material.value.strip():  # type: ignore
                    tf_descricao_material.error_text = "Requer preenchimento"
                else:
                    tf_descricao_material.error_text = None
                    descricao_material_valida = True
                validar_material()   
                page.update()

            # Validar Link Material Educativo
            def validar_link_material(e):
                nonlocal link_material_valida
                link_material_valida = False
                if not tf_link_material.value.strip():  # type: ignore
                    tf_link_material.error_text = "Requer preenchimento"
                else:
                    tf_link_material.error_text = None
                    link_material_valida = True
                validar_material()   
                page.update()

            # Validar Material Educativo
            def validar_material():
                nonlocal descricao_material_valida
                nonlocal link_material_valida
                material_validado = all([
                    descricao_material_valida,
                    link_material_valida
                ])
                bt_criar_material.disabled = not material_validado

            # Validar Descrição Material Educativo Edição
            def validar_descricao_material_e(e):
                nonlocal descricao_material_valida
                descricao_material_valida = True
                if not tf_descricao_material.value.strip():  # type: ignore
                    tf_descricao_material.error_text = "Requer preenchimento"
                    descricao_material_valida = False
                else:
                    tf_descricao_material.error_text = None
                    decricao_material_valida = True
                validar_material_e()   
                page.update()

            # Validar Link Material Educativo Edição
            def validar_link_material_e(e):
                nonlocal link_material_valida
                link_material_valida = True
                if not tf_link_material.value.strip():  # type: ignore
                    tf_link_material.error_text = "Requer preenchimento"
                    link_material_valida = False
                else:
                    tf_link_material.error_text = None
                    link_material_valida = True
                validar_material_e()   
                page.update()

            # Validar Status Material Educativo Edição
            def validar_status_material_e(e):
                nonlocal status_material_valida
                status_material_valida = True
                if not dd_status_material.value.strip():  # type: ignore
                    dd_status_material.error_text = "Requer preenchimento"
                    status_material_valida = False
                else:
                    dd_status_material.error_text = None
                    status_material_valida = True
                validar_material_e()   
                page.update()

            # Validar Material Educativo Edição
            def validar_material_e():
                nonlocal descricao_material_valida
                nonlocal link_material_valida
                nonlocal status_material_valida
                material_validado = all([
                    descricao_material_valida,
                    link_material_valida,
                    status_material_valida
                ])
                bt_editar_material.disabled = not material_validado

            # Acompanhar Denúncia de Bullying (Novo Comentário)
            def novo_comentario(e):
                global denuncia_id
                global usuario_id
                global status
                denuncia = bd.buscar_denuncia_por_id(denuncia_id)
                if denuncia != None:
                    bd.criar_denuncia_comentario(denuncia_id, tf_comentario.value, usuario_id, denuncia["Status"]) # type: ignore
                    if not status == dd_status.value:
                        bd.atualizar_denuncia(denuncia_id, status=dd_status.value)
                        bd.criar_log(f"Alterado Status [{status}] => [{dd_status.value}] da Denúncia N° [{denuncia_id}]", usuario_id)
                return page.go("/acompanhar")

            # Mudar Senha Usuário
            def mudar_senha(e):
                global usuario_id
                global usuario_nome
                global usuario_tipo
                global usuario_email
                usuario = bd.buscar_usuario_por_id(usuario_id) # type: ignore
                if usuario == None:
                    lb_erro_muda_senha.value = "Usuário inválido"
                    page.update()
                    return None
                else:
                    if utilidades.verificar_hash_bcrypt(tf_senha_atual.value, usuario["Senha"]): # type: ignore
                       bd.atualizar_usuario(usuario_id, senha=utilidades.gerar_hash_bcrypt(tf_senha_nova.value)) # type: ignore
                       bd.criar_log(f"Alterada a Senha do Usuário Id [{usuario_id}]", usuario_id)
                       return page.go("/menu")
                    else:
                       lb_erro_muda_senha.value = "Senha Atual inválida"
                       page.update()
                       return None

            # Validar Mensagem
            def validar_mensagem(e):
                nonlocal mensagem_valida
                mensagem_valida = False
                mensagem = tf_mensagem.value
                erros = []
                # Verifica cada requisito individualmente
                if mensagem:
                    if len(mensagem) < 1:
                        erros.append("Mínimo 1 caractere")
                else:
                    erros.append("Mensagem requerida")
                if erros:
                   mensagem_valida = False
                   tf_mensagem.error_text = "Mensagem inválida"
                else:
                   mensagem_valida = True
                   tf_mensagem.error_text = None
                bt_enviar_reuniao.disabled = not mensagem_valida
                page.update()

            # Enivar mensagem Reunião
            def envia_reuniao(e):
                global denuncia_id
                global data_reuniao
                global flag_thread
                global usuario_id
                bd.criar_denuncia_reuniao(denuncia_id, tf_mensagem.value, usuario_id) # type: ignore
                tf_mensagem.value = ""
                bt_enviar_reuniao.disabled = True
                page.update()

            # Autorefresh Reunião
            async def auto_reuniao(ct_reuniao, page):
                global lv_reuniao
                global flag_atualiza
                global flag_thread
                while flag_thread:
                    # print(f"Auto {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} {flag_atualiza}")
                    atualizar_reuniao(True)
                    if flag_atualiza:
                        flag_atualiza = False
                        ct_reuniao.content.controls = [lv_reuniao]
                        page.update()
                    await asyncio.sleep(1)  # Espera 1 segundos antes de atualizar novamente

            # Sair Reunião
            def sair_reuniao(e):
                global flag_thread
                flag_thread = False
                return page.go("/acompanhar")

            # Atualizar Reunião
            def atualizar_reuniao(fazer):
                global denuncia_id
                global reuniao_id
                global data_reuniao
                global lv_reuniao
                global flag_atualiza
                global flag_thread
                
                aux_reuniao_id = 0
                reuniao = bd.listar_denuncias_reuniao_usuario(denuncia_id=denuncia_id, denuncia_reuniao_id=reuniao_id, data=data_reuniao)

                for msg in reuniao:
                    # Container para cada mensagem
                    ct_reuniao = ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(msg["UsuarioTipo"] if msg["UsuarioTipo"] == "Denunciante" else f'{msg["UsuarioTipo"]} - {msg["UsuarioNome"]}', weight=ft.FontWeight.BOLD),
                                ft.Text(msg["Mensagem"], size=14),
                                ft.Text(datetime.fromisoformat(msg["DataHora"]).strftime(FORMATO_DATA_HORA), size=10, color=ft.Colors.GREY),
                            ],
                            spacing=2,
                        ),
                        padding=10,
                        border_radius=10,
                        bgcolor="#8CDF7C" if msg["UsuarioTipo"] == "Denunciante" else "#B3E6A3",
                        margin=ft.margin.only(left=50 if msg["UsuarioTipo"] == "Denunciante" else 0, right=0 if msg["UsuarioTipo"] == "Denunciante" else 50),
                        alignment=ft.alignment.center_left if msg["UsuarioTipo"] == "Denunciante" else ft.alignment.center_right,
                        expand=True,
                    )
                    # Adicionar à lista de itens
                    itens_reuniao.append(ct_reuniao)
                    aux_reuniao_id = msg["DenunciaReuniaoId"]
                # Criar ListView com expansão
                lv_reuniao = ft.ListView(
                    controls=itens_reuniao,
                    spacing=10,
                    expand=True,  # Isso faz o ListView ocupar todo o espaço disponível
                    auto_scroll=True,
                )
                # print(reuniao_id, aux_reuniao_id)    
                if fazer:
                    if aux_reuniao_id > reuniao_id:
                       reuniao_id = aux_reuniao_id
                       flag_atualiza = True
                else:
                    reuniao_id = aux_reuniao_id

            # Criar containers para cada célula com largura fixa
            def criar_celula(conteudo, largura=None, alinhamento=ft.alignment.center_left):
                return ft.Container(
                    content=conteudo,
                    width=largura,
                    padding=10,
                    alignment=alinhamento,
                )

            # Seleciona Usuário
            def seleciona_usuario(e, select_usuario):
                global w_usuario_id
                w_usuario_id = select_usuario
                return page.go("/usuario")

            # Criar Usuário
            def criar_usuario(e):
                usuario = bd.buscar_usuario_por_email(tf_email_usuario.value) # type: ignore
                if not usuario == None:
                    lb_erro_usuario.value = "Email do Usuário já existe"
                    page.update()
                    return None
                else:
                    senha_gerada = utilidades.gerar_senha_forte(12)
                    aux_usuario_id = bd.criar_usuario(tf_email_usuario.value, utilidades.gerar_hash_bcrypt(senha_gerada), tf_nome_usuario.value, dd_tipo_usuario.value, "Ativo") # type: ignore
                    bd.criar_log(f"Criado o Usuário [{aux_usuario_id}] [{tf_email_usuario.value}] [{tf_nome_usuario.value}]", usuario_id)
                    ret=utilidades.envia_email(tf_nome_usuario.value,tf_email_usuario.value, senha_gerada)
                    print(ret)
                    return page.go("/cadastrousuarios")

            # Seleciona Editar Usuário 
            def seleciona_editar_usuario(e, select_usuario):
                global w_usuario_id
                w_usuario_id = select_usuario
                return page.go("/editarusuario")

            # Seleciona Apagar Usuário 
            def seleciona_apagar_usuario(e, select_usuario):
                global w_usuario_id
                w_usuario_id = select_usuario
                return page.go("/apagarusuario")

            # Seleciona Resetar Senha Usuário 
            def seleciona_resetar_usuario(e, select_usuario):
                global w_usuario_id
                w_usuario_id = select_usuario
                return page.go("/resetarusuario")

            # Editar Usuário
            def editar_usuario(e):
                global usuario_id
                global w_usuario_id
                usuario = bd.buscar_usuario_por_id(w_usuario_id) # type: ignore
                if usuario == None:
                    lb_erro_usuario.value = "Usuário não existe"
                    page.update()
                    return None
                else:
                   bd.atualizar_usuario(w_usuario_id, nome=tf_nome_usuario.value, tipo=dd_tipo_usuario.value, status=dd_status_usuario.value) # type: ignore
                   bd.criar_log(f"Editado o Usuário [{w_usuario_id}] [{usuario['Email']}] ([{usuario['Nome']}] => [{tf_nome_usuario.value}]) ([{usuario['Tipo']}] => [{dd_tipo_usuario.value}]) ([{usuario['Status']}] => [{dd_status_usuario.value}])", usuario_id)
                return page.go("/cadastrousuarios")

            # Apagar Usuário
            def apagar_usuario(e):
                global usuario_id
                global w_usuario_id
                usuario = bd.buscar_usuario_por_id(w_usuario_id) # type: ignore
                if usuario == None:
                    lb_erro_usuario.value = "Usuário não existe"
                    page.update()
                    return None
                else:
                   bd.deletar_usuario(w_usuario_id) # type: ignore
                   bd.criar_log(f"Apagado o Usuário [{w_usuario_id}] [{usuario['Email']}] ([{usuario['Nome']}]", usuario_id)
                return page.go("/cadastrousuarios")

            # Resetar Usuário
            def resetar_usuario(e):
                global usuario_id
                global w_usuario_id
                usuario = bd.buscar_usuario_por_id(w_usuario_id) # type: ignore
                if usuario == None:
                    lb_erro_usuario.value = "Usuário não existe"
                    page.update()
                    return None
                else:
                   senha_gerada = utilidades.gerar_senha_forte(12)
                   bd.atualizar_usuario(w_usuario_id, senha=utilidades.gerar_hash_bcrypt(senha_gerada)) # type: ignore
                   bd.criar_log(f"Resetada a Senha do Usuário [{w_usuario_id}] [{usuario['Email']}] ([{usuario['Nome']}]", usuario_id)
                   ret=utilidades.envia_email(usuario['Nome'], usuario['Email'], senha_gerada)
                   print(ret)

                return page.go("/cadastrousuarios")

            # Seleciona Material Educativo
            def seleciona_material(e, select_material):
                global w_material_id
                w_material_id = select_material
                return page.go("/material")

            # Criar Material Educativo
            def criar_material(e):
                global usuario_id
                aux_material_id = bd.criar_material_educativo(tf_descricao_material.value, tf_link_material.value, usuario_id, 0, "Ativo") # type: ignore
                bd.criar_log(f"Criado o Material Educativo [{aux_material_id}]", usuario_id)
                return page.go("/cadastromateriais")

            # Seleciona Editar Material Educativo 
            def seleciona_editar_material(e, select_material):
                global w_material_id
                w_material_id = select_material
                return page.go("/editarmaterial")

            # Seleciona Apagar Material Educativo 
            def seleciona_apagar_material(e, select_material):
                global w_material_id
                w_material_id = select_material
                return page.go("/apagarmaterial")

            # Editar Material Educativo
            def editar_material(e):
                global usuario_id
                global w_material_id
                print("1", w_material_id)
                material = bd.buscar_material_educativo_por_id(w_material_id) # type: ignore
                if material == None:
                    lb_erro_material.value = "Material Educativo não existe"
                    page.update()
                    return None
                else:
                   bd.atualizar_material_educativo(w_material_id, descricao=tf_descricao_material.value, link=tf_link_material.value, usuario_id_alterou=usuario_id, status=dd_status_material.value) # type: ignore
                   bd.criar_log(f"Editado o Material Educativo [{w_material_id}] ([{material['Descricao']}] => [{tf_descricao_material.value}]) ([{material['Link']}] => [{tf_link_material.value}]) ([{material['Status']}] => [{dd_status_material.value}])", usuario_id)
                return page.go("/cadastromateriais")

            # Apagar Material Educativo
            def apagar_material(e):
                global usuario_id
                global w_material_id
                material = bd.buscar_material_educativo_por_id(w_material_id) # type: ignore
                if material == None:
                    lb_erro_material.value = "Material Educativo não existe"
                    page.update()
                    return None
                else:
                   bd.deletar_material_educativo(w_material_id) # type: ignore
                   bd.criar_log(f"Apagado o Material Educativo [{w_material_id}] [{material['Descricao']}]", usuario_id)
                return page.go("/cadastromateriais")

            ######################## 
            # Página Inicial (Login)
            email_valida = False
            senha_valida = False
            tf_email = ft.TextField(label="Email do Usuário", on_change=validar_email)
            tf_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, on_change=validar_senha)
            lb_erro = ft.Text("", color=ft.Colors.RED)
            # bt_login = ft.ElevatedButton("Login", style=button_style, on_click=login, icon=ft.Icons.LOCK, disabled=True)
            bt_login = ft.ElevatedButton("Login", style=button_style, on_click=login, icon=ft.Icons.LOCK, disabled=True)
            
            # tf_email.value = "msrs@cesar.school"
            # tf_senha.value = "Mauro#12"

            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.AppBar(title=ft.Text("Denúncia de Bullying Anônima - Gerencial"), color=ft.Colors.BLACK, bgcolor="#2E9239"),
                        ft.Row(
                            controls=[ft.Text("Informar o email e senha do usuário para ter acesso ao Gerencial.", weight=ft.FontWeight.BOLD)],
                            alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                        ),
                        ft.Row(
                            controls=[tf_email],
                            alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                        ),
                        ft.Row(
                            controls=[tf_senha],
                            alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                        ),
                        ft.Row(
                            controls=[lb_erro],
                            alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                        ),
                        ft.Row(
                            controls=[bt_login],
                            alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                        ),
                    ],
                )
            )

            # Menu
            if page.route == "/menu":
                page.views.append(
                   ft.View(
                        "/menu",
                        [
                            ft.AppBar(title=ft.Text("Denúncia de Bullying Anônima - Gerencial"), 
                                    color=ft.Colors.BLACK, 
                                    bgcolor="#2E9239",
                                    center_title=False,
                                    actions=[
                                        ft.Container(
                                            content=ft.Row([
                                                ft.Column([
                                                    ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                    ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                    ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                    ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                    ], spacing=1),
                                                # ft.Icon(ft.Icons.PERSON)
                                                ft.IconButton(
                                                    ft.Icons.PERSON,
                                                    # icon_color=ft.Colors.BLUE_700,
                                                    tooltip="Mudar Senha Usuário",
                                                    on_click=lambda _: page.go("/mudarsenha")
                                                    )
                                            ], 
                                            spacing=2,
                                            ),
                                            padding=ft.padding.only(right=20)
                                        )
                                    ],
                                    leading=ft.IconButton(
                                      icon=ft.Icons.ARROW_BACK,
                                      tooltip="Voltar",  # Tooltip modificado
                                      on_click=lambda _: page.go("/"),  # Comportamento de voltar padrão
                                    ),
                                ),
                            ft.Row(
                                    controls=[ft.Image(src="assets/logo.jpg", width=200,height=200)],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                            ft.Row(
                                    controls=[ft.ElevatedButton("Acompanhar as Denúncias de Bullying", style=button_style, on_click=lambda _: page.go("/acompanhardenuncia"), icon=ft.Icons.APPS_OUTAGE)],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                            ft.Row(
                                    controls=[ft.ElevatedButton("Cadastro de Materiais Educativos", style=button_style, on_click=lambda _: page.go("/cadastromateriais"), icon=ft.Icons.CASES_ROUNDED)],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                            ft.Row(
                                    controls=[ft.ElevatedButton("Cadastro de Usuários", style=button_style, on_click=lambda _: page.go("/cadastrousuarios"), icon=ft.Icons.SUPERVISED_USER_CIRCLE)],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                            ft.Row(
                                    controls=[ft.ElevatedButton("Visualizar Log", style=button_style, on_click=lambda _: page.go("/visualizarlog"), icon=ft.Icons.REPORT)],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                        ],
                    )
                )

            # Página Acompanhar Denúncia de Bullying
            if page.route == "/acompanhardenuncia":
                # Cabeçalho fixo
                cabecalho = ft.Row(
                    controls=[
                        criar_celula(ft.Text("N° Denúncia", weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                        criar_celula(ft.Text("Data e Hora", weight=ft.FontWeight.BOLD), 120, ft.alignment.top_center),
                        criar_celula(ft.Text("Descrição", weight=ft.FontWeight.BOLD), 650, ft.alignment.top_center),
                        criar_celula(ft.Text("Status", weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                        criar_celula(ft.Text("", weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                    ],
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.START
                )
                denuncias = bd.listar_denuncias()
                # Corpo da tabela com scroll
                linhas = []
                zebrado = False
                for den in denuncias:
                    cor = ft.Colors.BLACK
                    if den["Status"] == "Aberta": # type: ignore
                        cor = ft.Colors.RED
                    elif den["Status"] == "Em Atendimento": # type: ignore
                        cor = ft.Colors.BLUE
                    elif den["Status"] == "Encerrada": # type: ignore
                        cor = ft.Colors.GREEN
                    data_obj = datetime.strptime(den["DataHora"], FORMATO_DATA_HORA_ISO)
                    data_formatada = data_obj.strftime(FORMATO_DATA_HORA)
                    if zebrado:
                        cor_zebrado = "#D4F1C1"
                    else:
                        cor_zebrado = ft.Colors.WHITE
                    zebrado = not zebrado
                    linhas.append(
                        ft.Container(
                            ft.Row(
                                controls=[
                                    criar_celula(ft.Text(den["DenunciaId"], weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                                    criar_celula(ft.Text(data_formatada), 120, ft.alignment.top_center),
                                    criar_celula(
                                        ft.Text(
                                            den["DescricaoOque"],
                                            max_lines=2,
                                            overflow=ft.TextOverflow.ELLIPSIS,
                                            tooltip=den["DescricaoOque"],
                                            selectable=True,
                                        ), 
                                        650
                                    ),
                                    criar_celula(ft.Text(den["Status"], color=cor, weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                                    criar_celula(
                                        ft.IconButton(
                                            ft.Icons.SELECT_ALL,
                                            icon_color=ft.Colors.BLACK,
                                            tooltip="Selecionar Denúncia",
                                            on_click=lambda e, select_denuncia=den["DenunciaId"]: seleciona_denuncia(e, select_denuncia)
                                            ),
                                        150, ft.alignment.top_center
                                    )
                                ],
                                spacing=0,
                                vertical_alignment=ft.CrossAxisAlignment.START
                            ),
                            bgcolor=cor_zebrado,
                            padding=0,
                            border=ft.border.only(
                                top=ft.border.BorderSide(1, "#D4F1C1"),
                                # left=ft.border.BorderSide(1, "#D4F1C1"),
                                # right=ft.border.BorderSide(1, "#D4F1C1")
                            )
                        )
                    )
                # Tabela completa
                tabela = ft.Column(
                    controls=[
                        # Cabeçalho fixo
                        ft.Container(
                            cabecalho,
                            bgcolor="#8CDF7C",
                            padding=10,
                            border=ft.border.only(
                                top=ft.border.BorderSide(1, "#D4F1C1"),
                                left=ft.border.BorderSide(1, "#D4F1C1"),
                                right=ft.border.BorderSide(1, "#D4F1C1")
                            )
                        ),
                        # Corpo com scroll
                        ft.Container(
                            content=ft.ListView(
                                controls=linhas,
                                expand=True,
                                spacing=0,
                                padding=0,
                            ),
                            border=ft.border.only(
                                bottom=ft.border.BorderSide(1, "#D4F1C1"),
                                left=ft.border.BorderSide(1, "#D4F1C1"),
                                right=ft.border.BorderSide(1, "#D4F1C1")
                            ),
                            expand=True
                        )
                    ],
                    spacing=0,
                    expand=True
                )
                page.views.append(
                   ft.View(
                        "/acompanhar",
                        [
                            ft.AppBar(title=ft.Text(f"Acompanhar Denúncia de Bullying"), 
                                    color=ft.Colors.BLACK, 
                                    bgcolor="#2E9239",
                                    center_title=False,
                                    actions=[
                                        ft.Container(
                                            content=ft.Row([
                                                ft.Column([
                                                    ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                    ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                    ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                    ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                    ], spacing=1),
                                                # ft.Icon(ft.Icons.PERSON)
                                                ft.IconButton(
                                                    ft.Icons.PERSON,
                                                    # icon_color=ft.Colors.BLUE_700,
                                                    tooltip="Mudar Senha Usuário",
                                                    on_click=lambda _: page.go("/mudarsenha")
                                                    )
                                            ], 
                                            spacing=2,
                                            ),
                                            padding=ft.padding.only(right=20)
                                        )
                                    ],
                                  leading=ft.IconButton(
                                      icon=ft.Icons.ARROW_BACK,
                                      tooltip="Voltar",  # Tooltip modificado
                                      on_click=lambda _: page.go("/menu"),  # Comportamento de voltar padrão
                                    ),
                                ),
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        tabela,
                                        expand=True,
                                        border_radius=0,
                                    ),
                                ],
                                expand=True,
                            )
                        ],
                    )
                )

            # Página Acompanhar Denúncia de Bullying
            if page.route == "/acompanhar":
                denuncia = bd.buscar_denuncia_por_id(denuncia_id)
                status = denuncia["Status"] # type: ignore
                tf_v_n_denuncia = ft.TextField(label="Número da Denúncia", value=str(denuncia_id), read_only=True)
                tf_v_datahora = ft.TextField(label="Data e Hora", value=datetime.fromisoformat(denuncia["DataHora"]).strftime(FORMATO_DATA_HORA), read_only=True) # type: ignore
                tf_v_descricao_o_que = ft.TextField(label="Descrição - O que?", value=denuncia["DescricaoOque"], read_only=True, multiline=True, width=610, max_lines=3) # type: ignore
                tf_v_descricao_como_se_sente = ft.TextField(label="Descrição - Como se sente?", value=denuncia["DescricaoComoSeSente"], read_only=True, multiline=True, width=610, max_lines=3) # type: ignore
                tf_v_local = ft.TextField(label="Local", value=denuncia["Local"], read_only=True) # type: ignore
                tf_v_frequencia = ft.TextField(label="Frequência", value=denuncia["Frequencia"], read_only=True) # type: ignore
                tf_v_tipo_bullying = ft.TextField(label="Tipo Bullying", value=denuncia["TipoBullying"], read_only=True) # type: ignore
                cor = ft.Colors.BLACK
                if denuncia["Status"] == "Aberta": # type: ignore
                    cor = ft.Colors.RED
                elif denuncia["Status"] == "Em Atendimento": # type: ignore
                    cor = ft.Colors.BLUE
                elif denuncia["Status"] == "Encerrada": # type: ignore
                    cor = ft.Colors.GREEN
                tf_v_status = ft.TextField(label="Status", value=denuncia["Status"], read_only=True, color=cor) # type: ignore
                denuncia_comentarios = bd.listar_denuncias_comentarios_usuario(denuncia_id=denuncia_id)
                bt_novo_comentario = ft.ElevatedButton("Novo Comentário", style=button_style, on_click=lambda _: page.go("/acompanharnovocomentario"), icon=ft.Icons.ADD_COMMENT)
                bt_reuniao = ft.ElevatedButton("Reuniao", style=button_style, on_click=lambda _: page.go("/reuniao"), icon=ft.Icons.INSERT_COMMENT)
                # Criar itens da lista de comentário
                itens_comentarios = []
                for msg in denuncia_comentarios:
                    # Container para cada comentário
                    ct_comentario = ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(msg["UsuarioTipo"] if msg["UsuarioTipo"] == "Denunciante" else f'{msg["UsuarioTipo"]} - {msg["UsuarioNome"]}', weight=ft.FontWeight.BOLD),
                                ft.Text(msg["Comentario"], size=14),
                                ft.Text(datetime.fromisoformat(msg["DataHora"]).strftime(FORMATO_DATA_HORA), size=10, color=ft.Colors.GREY),
                            ],
                            spacing=2,
                        ),
                        padding=10,
                        border_radius=10,
                        bgcolor="#8CDF7C" if msg["UsuarioTipo"] == "Denunciante" else "#B3E6A3",
                        margin=ft.margin.only(left=50 if msg["UsuarioTipo"] == "Denunciante" else 0, right=0 if msg["UsuarioTipo"] == "Denunciante" else 50),
                        alignment=ft.alignment.center_left if msg["UsuarioTipo"] == "Denunciante" else ft.alignment.center_right,
                        expand=True,
                    )
                    # Adicionar à lista de itens
                    itens_comentarios.append(ct_comentario)
                # Criar ListView com expansão
                lv_comentarios = ft.ListView(
                    controls=itens_comentarios,
                    spacing=10,
                    expand=True,  # Isso faz o ListView ocupar todo o espaço disponível
                    auto_scroll=True,
                )
                page.views.append(
                   ft.View(
                        "/acompanhar",
                        [
                            ft.AppBar(
                                title=ft.Text("Acompanhar Denúncia de Bullying"),
                                color=ft.Colors.BLACK, 
                                bgcolor="#2E9239",
                                actions=[
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Column([
                                                ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                ], spacing=1),
                                            # ft.Icon(ft.Icons.PERSON)
                                            ft.IconButton(
                                                ft.Icons.PERSON,
                                                # icon_color=ft.Colors.BLUE_700,
                                                tooltip="Mudar Senha Usuário",
                                                on_click=lambda _: page.go("/mudarsenha")
                                                )
                                        ], 
                                        spacing=2,
                                        ),
                                        padding=ft.padding.only(right=20)
                                    )
                                ],
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/acompanhardenuncia"),  # Comportamento de voltar padrão
                                ),
                            ),
                            # ft.Container(content=ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, controls=[
                                ft.Row(
                                    controls=[tf_v_n_denuncia, tf_v_datahora],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_descricao_o_que],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_descricao_como_se_sente],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_local, tf_v_frequencia],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_tipo_bullying, tf_v_status],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[ft.Text("Comentários", weight=ft.FontWeight.BOLD), bt_novo_comentario, bt_reuniao],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Container(
                                    content=lv_comentarios,
                                    expand=True,
                                    border=ft.border.all(1, ft.Colors.GREY_300),
                                    border_radius=10,
                                    padding=10,
                                ),
                            # ]), expand=True, padding=10),
                        ],
                    )
                )
            
            # Página Acompanhar Denúncia de Bullying Novo Comentário
            if page.route == "/acompanharnovocomentario":
                comentario_valida = False
                status_valida = True
                tf_v_n_denuncia = ft.TextField(label="Número da Denúncia", value=str(denuncia_id), read_only=True)
                tf_comentario = ft.TextField(label="Comentário", multiline=True, width=610, on_change=validar_comentario)
                dd_status = ft.Dropdown(label="Status", 
                                                options=[
                                                    ft.dropdown.Option("Aberta"),
                                                    ft.dropdown.Option("Em Atendimento"),
                                                    ft.dropdown.Option("Encerrada"),
                                            ], on_change=validar_status, value=status)
                bt_salvar_comentario = ft.ElevatedButton("Salvar Comentário", style=button_style, disabled=True, on_click=novo_comentario, icon=ft.Icons.DATA_SAVER_ON)
                page.views.append(
                   ft.View(
                        "/acompanharnovocomentario",
                        [
                            ft.AppBar(
                                title=ft.Text("Acompanhar Denúncia de Bullying (Novo Comentário)"),
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/acompanhar"),  # Comportamento de voltar padrão
                                ),
                                color=ft.Colors.BLACK, 
                                bgcolor="#2E9239",
                                actions=[
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Column([
                                                ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                ], spacing=1),
                                            # ft.Icon(ft.Icons.PERSON)
                                            ft.IconButton(
                                                ft.Icons.PERSON,
                                                # icon_color=ft.Colors.BLUE_700,
                                                tooltip="Mudar Senha Usuário",
                                                on_click=lambda _: page.go("/mudarsenha")
                                                )
                                        ], 
                                        spacing=2,
                                        ),
                                        padding=ft.padding.only(right=20)
                                    )
                                ],
                            ),
                            ft.Container(content=ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, controls=[
                                ft.Row(
                                    controls=[tf_v_n_denuncia],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_comentario],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[dd_status],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[bt_salvar_comentario],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                            ]), expand=True, padding=10),
                        ],
                   )
                )
            
            # Página Reunião
            if page.route == "/reuniao":
                reuniao_id = 0
                itens_reuniao = []
                data_reuniao = datetime.now().date()
                mensagem_valida = False
                tf_mensagem = ft.TextField(label="Mensagem", multiline=True, expand=True, on_change=validar_mensagem, max_lines=1)
                bt_enviar_reuniao = ft.ElevatedButton("Enviar mensagem", style=button_style, disabled=True, on_click=envia_reuniao, icon=ft.Icons.SEND)
                
                atualizar_reuniao(False)

                ct_reuniao = ft.Container(
                    content=lv_reuniao,
                    expand=True,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=10,
                    padding=10,
                )
                
                page.views.append(
                   ft.View(
                        "/reuniao",
                        [
                            ft.AppBar(
                                title=ft.Text(f"Reunião [{data_reuniao.strftime(FORMATO_DATA)}] [Denúncia N° {denuncia_id}]"),
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    # on_click=lambda _: page.go("/acompanhar"),  # Comportamento de voltar padrão
                                    on_click=sair_reuniao,  # Comportamento de voltar padrão
                                ),
                                color=ft.Colors.BLACK, 
                                bgcolor="#2E9239",
                                actions=[
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Column([
                                                ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                ], spacing=1),
                                            # ft.Icon(ft.Icons.PERSON)
                                            ft.IconButton(
                                                ft.Icons.PERSON,
                                                # icon_color=ft.Colors.BLUE_700,
                                                tooltip="Mudar Senha Usuário",
                                                on_click=lambda _: page.go("/mudarsenha")
                                                )
                                        ], 
                                        spacing=2,
                                        ),
                                        padding=ft.padding.only(right=20)
                                    )
                                ],
                            ),

                            ft.Row(
                                controls=[tf_mensagem, bt_enviar_reuniao],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                            ct_reuniao
                        ],
                    )
                )
                page.update()
                # Iniciar atualização automática
                flag_thread = True
                flag_thread_I = False
                asyncio.run(auto_reuniao(ct_reuniao, page))

            # Página Cadastro de Usuários
            if page.route == "/cadastrousuarios":
                flag_permissao = (usuario_tipo == "Administrador")
                # Cabeçalho fixo
                cabecalho = ft.Row(
                    controls=[
                        criar_celula(ft.Text("Id", weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                        criar_celula(ft.Text("Email", weight=ft.FontWeight.BOLD), 200, ft.alignment.top_center),
                        criar_celula(ft.Text("Nome", weight=ft.FontWeight.BOLD), 350, ft.alignment.top_center),
                        criar_celula(ft.Text("Tipo", weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                        criar_celula(ft.Text("Status", weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                        criar_celula(ft.Text("", weight=ft.FontWeight.BOLD), 200, ft.alignment.top_center),
                    ],
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.START
                )
                usuarios = bd.listar_usuarios()
                # Corpo da tabela com scroll
                linhas = []
                zebrado = False
                for usu in usuarios:
                    cor = ft.Colors.BLACK
                    if usu["Status"] == "Ativo": # type: ignore
                        cor = ft.Colors.GREEN
                    elif usu["Status"] == "Bloqueado": # type: ignore
                        cor = ft.Colors.ORANGE
                    elif usu["Status"] == "Cancelado": # type: ignore
                        cor = ft.Colors.RED
                    if zebrado:
                        cor_zebrado = "#D4F1C1"
                    else:
                        cor_zebrado = ft.Colors.WHITE
                    zebrado = not zebrado
                    linhas.append(
                        ft.Container(
                            ft.Row(
                                controls=[
                                    criar_celula(ft.Text(usu["UsuarioId"], weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                                    criar_celula(ft.Text(usu["Email"]), 200, ft.alignment.top_center),
                                    criar_celula(
                                        ft.Text(
                                            usu["Nome"],
                                            max_lines=2,
                                            overflow=ft.TextOverflow.ELLIPSIS,
                                            tooltip=usu["Nome"],
                                            selectable=True,
                                        ), 
                                        350
                                    ),
                                    criar_celula(ft.Text(usu["Tipo"]), 150, ft.alignment.top_center),
                                    criar_celula(ft.Text(usu["Status"], color=cor, weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                                    criar_celula(
                                                 ft.Row(
                                                     controls=[
                                                         ft.IconButton(
                                                             ft.Icons.SELECT_ALL,
                                                             icon_color=ft.Colors.BLACK,
                                                             tooltip="Visualiza Usuário",
                                                             on_click=lambda e, select_usuario=usu["UsuarioId"]: seleciona_usuario(e, select_usuario)
                                                         ),
                                                         ft.IconButton(
                                                             ft.Icons.EDIT_SHARP,
                                                             icon_color=ft.Colors.BLACK,
                                                             tooltip="Edita Usuário",
                                                             disabled=not flag_permissao,
                                                             on_click=lambda e, select_usuario=usu["UsuarioId"]: seleciona_editar_usuario(e, select_usuario)
                                                         ),
                                                         ft.IconButton(
                                                             ft.Icons.REMOVE_SHARP,
                                                             icon_color=ft.Colors.BLACK,
                                                             tooltip="Apaga Usuário",
                                                             disabled=not flag_permissao,
                                                             on_click=lambda e, select_usuario=usu["UsuarioId"]: seleciona_apagar_usuario(e, select_usuario)
                                                         ),
                                                         ft.IconButton(
                                                             ft.Icons.LOCK_RESET,
                                                             icon_color=ft.Colors.BLACK,
                                                             tooltip="Reseta Senha Usuário",
                                                             disabled=not flag_permissao,
                                                             on_click=lambda e, select_usuario=usu["UsuarioId"]: seleciona_resetar_usuario(e, select_usuario)
                                                         ),
                                                     ],
                                                     alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                                 ),
                                        200, ft.alignment.top_center
                                    )
                                ],
                                spacing=0,
                                vertical_alignment=ft.CrossAxisAlignment.START
                            ),
                            bgcolor=cor_zebrado,
                            padding=0,
                            border=ft.border.only(
                                top=ft.border.BorderSide(1, "#D4F1C1"),
                                # left=ft.border.BorderSide(1, "#D4F1C1"),
                                # right=ft.border.BorderSide(1, "#D4F1C1")
                            )
                        )
                    )
                # Tabela completa
                tabela = ft.Column(
                    controls=[
                        # Cabeçalho fixo
                        ft.Container(
                            cabecalho,
                            bgcolor="#8CDF7C",
                            padding=10,
                            border=ft.border.only(
                                top=ft.border.BorderSide(1, "#D4F1C1"),
                                left=ft.border.BorderSide(1, "#D4F1C1"),
                                right=ft.border.BorderSide(1, "#D4F1C1")
                            )
                        ),
                        # Corpo com scroll
                        ft.Container(
                            content=ft.ListView(
                                controls=linhas,
                                expand=True,
                                spacing=0,
                                padding=0,
                            ),
                            border=ft.border.only(
                                bottom=ft.border.BorderSide(1, ft.Colors.BLUE_400),
                                left=ft.border.BorderSide(1, ft.Colors.BLUE_400),
                                right=ft.border.BorderSide(1, ft.Colors.BLUE_400)
                            ),
                            expand=True
                        )
                    ],
                    spacing=0,
                    expand=True
                )
                page.views.append(
                   ft.View(
                        "/cadastrousuarios",
                        [
                            ft.AppBar(title=ft.Text(f"Cadastro de Usuários"), 
                                    color=ft.Colors.BLACK, 
                                    bgcolor="#2E9239",
                                    center_title=False,
                                    actions=[
                                        ft.Container(
                                            content=ft.Row([
                                                ft.Column([
                                                    ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                    ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                    ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                    ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                    ], spacing=1),
                                                # ft.Icon(ft.Icons.PERSON)
                                                ft.IconButton(
                                                    ft.Icons.PERSON,
                                                    # icon_color=ft.Colors.BLUE_700,
                                                    tooltip="Mudar Senha Usuário",
                                                    on_click=lambda _: page.go("/mudarsenha")
                                                    )
                                            ], 
                                            spacing=2,
                                            ),
                                            padding=ft.padding.only(right=20)
                                        )
                                    ],
                                  leading=ft.IconButton(
                                      icon=ft.Icons.ARROW_BACK,
                                      tooltip="Voltar",  # Tooltip modificado
                                      on_click=lambda _: page.go("/menu"),  # Comportamento de voltar padrão
                                    ),
                                ),
                            ft.Row(
                                    controls=[ft.ElevatedButton("Criar Usuário", style=button_style, disabled=not flag_permissao, on_click=lambda _: page.go("/criarusuario"), icon=ft.Icons.ADD_SHARP)],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        tabela,
                                        expand=True,
                                        border_radius=0,
                                    ),
                                ],
                                expand=True,
                            )
                        ],
                    )
                )

            # Página Visualizar Usuário
            if page.route == "/usuario":
                usuario = bd.buscar_usuario_por_id(w_usuario_id)
                tf_v_id = ft.TextField(label="Id", value=str(w_usuario_id), read_only=True)
                tf_v_email = ft.TextField(label="Email", value=usuario["Email"], read_only=True, width=610) # type: ignore
                tf_v_nome = ft.TextField(label="Nome", value=usuario["Nome"], read_only=True, multiline=True, width=610, max_lines=3) # type: ignore
                tf_v_tipo = ft.TextField(label="Tipo", value=usuario["Tipo"], read_only=True) # type: ignore
                cor = ft.Colors.BLACK
                if usuario["Status"] == "Ativo": # type: ignore
                    cor = ft.Colors.GREEN
                elif usuario["Status"] == "Bloqueado": # type: ignore
                    cor = ft.Colors.ORANGE
                elif usuario["Status"] == "Cancelado": # type: ignore
                    cor = ft.Colors.RED
                tf_v_status_u = ft.TextField(label="Status", value=usuario["Status"], read_only=True, color=cor) # type: ignore

                page.views.append(
                   ft.View(
                        "/usuario",
                        [
                            ft.AppBar(
                                title=ft.Text("Visualiza Usuário"),
                                color=ft.Colors.BLACK, 
                                bgcolor="#2E9239",
                                actions=[
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Column([
                                                ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                ], spacing=1),
                                            # ft.Icon(ft.Icons.PERSON)
                                            ft.IconButton(
                                                ft.Icons.PERSON,
                                                # icon_color=ft.Colors.BLUE_700,
                                                tooltip="Mudar Senha Usuário",
                                                on_click=lambda _: page.go("/mudarsenha")
                                                )
                                        ], 
                                        spacing=2,
                                        ),
                                        padding=ft.padding.only(right=20)
                                    )
                                ],
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/cadastrousuarios"),  # Comportamento de voltar padrão
                                ),
                            ),
                            # ft.Container(content=ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, controls=[
                                ft.Row(
                                    controls=[tf_v_id],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_email],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_nome],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_tipo, tf_v_status_u],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                            # ]), expand=True, padding=10),
                        ],
                    )
                )

            # Página Criar Usuário
            if page.route == "/criarusuario":
                email_usuario_valida = False
                nome_usuario_valida = False
                tipo_usuario_valida = False

                tf_email_usuario = ft.TextField(label="Email", width=610, on_change=validar_email_usuario) # type: ignore
                tf_nome_usuario = ft.TextField(label="Nome", multiline=True, width=610, max_lines=3, on_change=validar_nome_usuario)  # type: ignore
                dd_tipo_usuario = ft.Dropdown(label="Tipo", 
                                      options=[
                                          ft.dropdown.Option("Administrador"),
                                          ft.dropdown.Option("Diretor"),
                                          ft.dropdown.Option("Psicólogo"),
                                          ], 
                                      on_change=validar_tipo_usuario)
                lb_erro_usuario = ft.Text("", color=ft.Colors.RED)
                bt_criar_usuario = ft.ElevatedButton("Salvar", style=button_style, on_click=criar_usuario, icon=ft.Icons.SAVE_ALT_SHARP, disabled=True)

                page.views.append(
                   ft.View(
                        "/criarusuario",
                        [
                            ft.AppBar(
                                title=ft.Text("Criar Usuário"),
                                color=ft.Colors.BLACK, 
                                bgcolor="#2E9239",
                                actions=[
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Column([
                                                ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                ], spacing=1),
                                            # ft.Icon(ft.Icons.PERSON)
                                            ft.IconButton(
                                                ft.Icons.PERSON,
                                                # icon_color=ft.Colors.BLUE_700,
                                                tooltip="Mudar Senha Usuário",
                                                on_click=lambda _: page.go("/mudarsenha")
                                                )
                                        ], 
                                        spacing=2,
                                        ),
                                        padding=ft.padding.only(right=20)
                                    )
                                ],
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/cadastrousuarios"),  # Comportamento de voltar padrão
                                ),
                            ),
                            # ft.Container(content=ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, controls=[
                                ft.Row(
                                    controls=[tf_email_usuario],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_nome_usuario],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[dd_tipo_usuario],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[lb_erro_usuario],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[bt_criar_usuario],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                            # ]), expand=True, padding=10),
                        ],
                    )
                )

            # Página Editar Usuário
            if page.route == "/editarusuario":
                nome_usuario_valida = True
                tipo_usuario_valida = True
                status_usuario_valida = True
                usuario = bd.buscar_usuario_por_id(w_usuario_id)
                tf_v_id = ft.TextField(label="Id", value=str(w_usuario_id), read_only=True)
                tf_v_email = ft.TextField(label="Email", value=usuario["Email"], read_only=True, width=610) # type: ignore
                tf_nome_usuario = ft.TextField(label="Nome", value=usuario["Nome"], multiline=True, width=610, max_lines=3, on_change=validar_nome_usuario_e)  # type: ignore
                dd_tipo_usuario = ft.Dropdown(label="Tipo", 
                                      options=[
                                          ft.dropdown.Option("Administrador"),
                                          ft.dropdown.Option("Diretor"),
                                          ft.dropdown.Option("Psicólogo"),
                                          ], 
                                      value=usuario["Tipo"],  # type: ignore
                                      on_change=validar_tipo_usuario_e)
                dd_status_usuario = ft.Dropdown(label="Status", 
                                      options=[
                                          ft.dropdown.Option("Ativo"),
                                          ft.dropdown.Option("Bloqueado"),
                                          ft.dropdown.Option("Cancelado"),
                                          ], 
                                      value=usuario["Status"],   # type: ignore
                                      on_change=validar_status_usuario_e)
                lb_erro_usuario = ft.Text("", color=ft.Colors.RED)
                bt_editar_usuario = ft.ElevatedButton("Salvar", style=button_style, on_click=editar_usuario, icon=ft.Icons.SAVE_ALT_SHARP, disabled=True)

                page.views.append(
                   ft.View(
                        "/editarusuario",
                        [
                            ft.AppBar(
                                title=ft.Text("Editar Usuário"),
                                color=ft.Colors.BLACK, 
                                bgcolor="#2E9239",
                                actions=[
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Column([
                                                ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                ], spacing=1),
                                            # ft.Icon(ft.Icons.PERSON)
                                            ft.IconButton(
                                                ft.Icons.PERSON,
                                                # icon_color=ft.Colors.BLUE_700,
                                                tooltip="Mudar Senha Usuário",
                                                on_click=lambda _: page.go("/mudarsenha")
                                                )
                                        ], 
                                        spacing=2,
                                        ),
                                        padding=ft.padding.only(right=20)
                                    )
                                ],
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/cadastrousuarios"),  # Comportamento de voltar padrão
                                ),
                            ),
                            # ft.Container(content=ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, controls=[

                                ft.Row(
                                    controls=[tf_v_id],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_email],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_nome_usuario],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[dd_tipo_usuario, dd_status_usuario],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[lb_erro_usuario],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[bt_editar_usuario],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                            # ]), expand=True, padding=10),
                        ],
                    )
                )

            # Página Apagar Usuário
            if page.route == "/apagarusuario":
                usuario = bd.buscar_usuario_por_id(w_usuario_id)
                tf_v_id = ft.TextField(label="Id", value=str(w_usuario_id), read_only=True)
                tf_v_email = ft.TextField(label="Email", value=usuario["Email"], read_only=True, width=610) # type: ignore
                tf_v_nome = ft.TextField(label="Nome", value=usuario["Nome"], read_only=True, multiline=True, width=610, max_lines=3) # type: ignore
                tf_v_tipo = ft.TextField(label="Tipo", value=usuario["Tipo"], read_only=True) # type: ignore
                cor = ft.Colors.BLACK
                if usuario["Status"] == "Ativo": # type: ignore
                    cor = ft.Colors.GREEN
                elif usuario["Status"] == "Bloqueado": # type: ignore
                    cor = ft.Colors.ORANGE
                elif usuario["Status"] == "Cancelado": # type: ignore
                    cor = ft.Colors.RED
                tf_v_status_u = ft.TextField(label="Status", value=usuario["Status"], read_only=True, color=cor) # type: ignore
                bt_apagar_usuario = ft.ElevatedButton("Apagar", style=button_style, on_click=apagar_usuario, icon=ft.Icons.DELETE)

                page.views.append(
                   ft.View(
                        "/apagarusuario",
                        [
                            ft.AppBar(
                                title=ft.Text("Apagar Usuário"),
                                color=ft.Colors.BLACK, 
                                bgcolor="#2E9239",
                                actions=[
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Column([
                                                ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                ], spacing=1),
                                            # ft.Icon(ft.Icons.PERSON)
                                            ft.IconButton(
                                                ft.Icons.PERSON,
                                                # icon_color=ft.Colors.BLUE_700,
                                                tooltip="Mudar Senha Usuário",
                                                on_click=lambda _: page.go("/mudarsenha")
                                                )
                                        ], 
                                        spacing=2,
                                        ),
                                        padding=ft.padding.only(right=20)
                                    )
                                ],
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/cadastrousuarios"),  # Comportamento de voltar padrão
                                ),
                            ),
                            # ft.Container(content=ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, controls=[
                                ft.Row(
                                    controls=[tf_v_id],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_email],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_nome],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_tipo, tf_v_status_u],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[ft.Text("Apagar o Usuário?", weight=ft.FontWeight.BOLD, color=ft.Colors.RED)],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[bt_apagar_usuario],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                            # ]), expand=True, padding=10),
                        ],
                    )
                )

            # Página Resetar Senha Usuário
            if page.route == "/resetarusuario":
                usuario = bd.buscar_usuario_por_id(w_usuario_id)
                tf_v_id = ft.TextField(label="Id", value=str(w_usuario_id), read_only=True)
                tf_v_email = ft.TextField(label="Email", value=usuario["Email"], read_only=True, width=610) # type: ignore
                tf_v_nome = ft.TextField(label="Nome", value=usuario["Nome"], read_only=True, multiline=True, width=610, max_lines=3) # type: ignore
                tf_v_tipo = ft.TextField(label="Tipo", value=usuario["Tipo"], read_only=True) # type: ignore
                cor = ft.Colors.BLACK
                if usuario["Status"] == "Ativo": # type: ignore
                    cor = ft.Colors.GREEN
                elif usuario["Status"] == "Bloqueado": # type: ignore
                    cor = ft.Colors.ORANGE
                elif usuario["Status"] == "Cancelado": # type: ignore
                    cor = ft.Colors.RED
                tf_v_status_u = ft.TextField(label="Status", value=usuario["Status"], read_only=True, color=cor) # type: ignore
                bt_apagar_usuario = ft.ElevatedButton("Resetar Senha", style=button_style, on_click=resetar_usuario, icon=ft.Icons.LOCK_RESET)

                page.views.append(
                   ft.View(
                        "/resetarusuario",
                        [
                            ft.AppBar(
                                title=ft.Text("Resetar Senha do Usuário"),
                                color=ft.Colors.BLACK, 
                                bgcolor="#2E9239",
                                actions=[
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Column([
                                                ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                ], spacing=1),
                                            # ft.Icon(ft.Icons.PERSON)
                                            ft.IconButton(
                                                ft.Icons.PERSON,
                                                # icon_color=ft.Colors.BLUE_700,
                                                tooltip="Mudar Senha Usuário",
                                                on_click=lambda _: page.go("/mudarsenha")
                                                )
                                        ], 
                                        spacing=2,
                                        ),
                                        padding=ft.padding.only(right=20)
                                    )
                                ],
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/cadastrousuarios"),  # Comportamento de voltar padrão
                                ),
                            ),
                            # ft.Container(content=ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, controls=[
                                ft.Row(
                                    controls=[tf_v_id],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_email],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_nome],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_tipo, tf_v_status_u],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[ft.Text("Resetar Senha do Usuário?", weight=ft.FontWeight.BOLD, color=ft.Colors.RED)],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[bt_apagar_usuario],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                            # ]), expand=True, padding=10),
                        ],
                    )
                )

            # Página Mudar Senha Usuario
            if page.route == "/mudarsenha":
                senha_atual_valida = False
                senha_nova_valida = False
                senha_nova_confirmar_valida = False
                tf_senha_atual = ft.TextField(label="Senha Atual", password=True, can_reveal_password=True, on_change=validar_senha_atual)
                tf_senha_nova = ft.TextField(label="Nova Senha", password=True, can_reveal_password=True, on_change=validar_senha_nova)
                cl_validacao_indicadores = ft.Column(spacing=5)
                tf_senha_nova_confirmar = ft.TextField(label="Confirmar a Senha", password=True, can_reveal_password=True, on_change=validar_senha_nova_confirmar)
                cl_validacao_indicadores_confirmar = ft.Column(spacing=5)
                lb_erro_muda_senha = ft.Text("", color=ft.Colors.RED)
                bt_mudar_senha = ft.ElevatedButton("Mudar Senha", style=button_style, on_click=mudar_senha, disabled=True, icon=ft.Icons.PUBLISHED_WITH_CHANGES)

                page.views.append(
                   ft.View(
                        "/mudarsenha",
                        [
                            ft.AppBar(
                                title=ft.Text(f"Mudar Senha do Usuário [{usuario_id}]"),
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/menu"),  # Comportamento de voltar padrão
                                ),
                                color=ft.Colors.BLACK, 
                                bgcolor="#2E9239",
                                actions=[
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Column([
                                                ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                ], spacing=1),
                                            # ft.Icon(ft.Icons.PERSON)
                                            ft.IconButton(
                                                ft.Icons.PERSON,
                                                # icon_color=ft.Colors.BLUE_700,
                                                tooltip="Mudar Senha Usuário",
                                                on_click=lambda _: page.go("/mudarsenha")
                                                )
                                        ], 
                                        spacing=2,
                                        ),
                                        padding=ft.padding.only(right=20)
                                    )
                                ],
                            ),
                            ft.Row(
                                controls=[tf_senha_atual],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                            ft.Row(
                                controls=[tf_senha_nova, cl_validacao_indicadores],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                            ft.Row(
                                controls=[tf_senha_nova_confirmar, cl_validacao_indicadores_confirmar],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                            ft.Row(
                                controls=[lb_erro_muda_senha],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                            ft.Row(
                                controls=[bt_mudar_senha],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                        ],
                    )
                )

            # Página Cadastro de Materiais Educativos
            if page.route == "/cadastromateriais":
                flag_permissao = True
                # Cabeçalho fixo
                cabecalho = ft.Row(
                    controls=[
                        criar_celula(ft.Text("Id", weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                        criar_celula(ft.Text("Descrição", weight=ft.FontWeight.BOLD), 550, ft.alignment.top_center),
                        criar_celula(ft.Text("Link", weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                        criar_celula(ft.Text("Status", weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                        criar_celula(ft.Text("", weight=ft.FontWeight.BOLD), 200, ft.alignment.top_center),
                    ],
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.START
                )
                materiais = bd.listar_materiais_educativos()
                # Corpo da tabela com scroll
                linhas = []
                zebrado = False
                for mat in materiais:
                    cor = ft.Colors.BLACK
                    if mat["Status"] == "Ativo": # type: ignore
                        cor = ft.Colors.GREEN
                    elif mat["Status"] == "Não Ativo": # type: ignore
                        cor = ft.Colors.RED
                    if zebrado:
                        cor_zebrado = "#D4F1C1"
                    else:
                        cor_zebrado = ft.Colors.WHITE
                    zebrado = not zebrado
                    linhas.append(
                        ft.Container(
                            ft.Row(
                                controls=[
                                    criar_celula(ft.Text(mat["MaterialId"], weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                                    criar_celula(
                                        ft.Text(
                                            mat["Descricao"],
                                            max_lines=3,
                                            overflow=ft.TextOverflow.ELLIPSIS,
                                            tooltip=mat["Descricao"],
                                            selectable=True,
                                        ), 
                                        550
                                    ),
                                    criar_celula(ft.IconButton(
                                                     ft.Icons.LINK,
                                                     icon_color=ft.Colors.BLACK,
                                                     tooltip="Link",
                                                     on_click=lambda e, link=mat["Link"]: webbrowser.open(link),
                                                    ), 150, ft.alignment.top_center),
                                    criar_celula(ft.Text(mat["Status"], color=cor, weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                                    criar_celula(
                                                 ft.Row(
                                                     controls=[
                                                         ft.IconButton(
                                                             ft.Icons.SELECT_ALL,
                                                             icon_color=ft.Colors.BLACK,
                                                             tooltip="Visualiza Material Educativo",
                                                             on_click=lambda e, select_material=mat["MaterialId"]: seleciona_material(e, select_material)
                                                         ),
                                                         ft.IconButton(
                                                             ft.Icons.EDIT_SHARP,
                                                             icon_color=ft.Colors.BLACK,
                                                             tooltip="Edita Material Eduicativo",
                                                             disabled=not flag_permissao,
                                                             on_click=lambda e, select_material=mat["MaterialId"]: seleciona_editar_material(e, select_material)
                                                         ),
                                                         ft.IconButton(
                                                             ft.Icons.REMOVE_SHARP,
                                                             icon_color=ft.Colors.BLACK,
                                                             tooltip="Apaga Material Educativo",
                                                             disabled=not flag_permissao,
                                                             on_click=lambda e, select_material=mat["MaterialId"]: seleciona_apagar_material(e, select_material)
                                                         ),
                                                     ],
                                                     alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                                 ),
                                        200, ft.alignment.top_center
                                    )
                                ],
                                spacing=0,
                                vertical_alignment=ft.CrossAxisAlignment.START
                            ),
                            bgcolor=cor_zebrado,
                            padding=0,
                            border=ft.border.only(
                                top=ft.border.BorderSide(1, "#D4F1C1"),
                                # left=ft.border.BorderSide(1, "#D4F1C1"),
                                # right=ft.border.BorderSide(1, "#D4F1C1")
                            )
                        )
                    )
                # Tabela completa
                tabela = ft.Column(
                    controls=[
                        # Cabeçalho fixo
                        ft.Container(
                            cabecalho,
                            bgcolor="#8CDF7C",
                            padding=10,
                            border=ft.border.only(
                                top=ft.border.BorderSide(1, "#D4F1C1"),
                                left=ft.border.BorderSide(1, "#D4F1C1"),
                                right=ft.border.BorderSide(1, "#D4F1C1")
                            )
                        ),
                        # Corpo com scroll
                        ft.Container(
                            content=ft.ListView(
                                controls=linhas,
                                expand=True,
                                spacing=0,
                                padding=0,
                            ),
                            border=ft.border.only(
                                bottom=ft.border.BorderSide(1, ft.Colors.BLUE_400),
                                left=ft.border.BorderSide(1, ft.Colors.BLUE_400),
                                right=ft.border.BorderSide(1, ft.Colors.BLUE_400)
                            ),
                            expand=True
                        )
                    ],
                    spacing=0,
                    expand=True
                )
                page.views.append(
                   ft.View(
                        "/cadastromateriais",
                        [
                            ft.AppBar(title=ft.Text(f"Cadastro de Materiais Educativos"), 
                                    color=ft.Colors.BLACK, 
                                    bgcolor="#2E9239",
                                    center_title=False,
                                    actions=[
                                        ft.Container(
                                            content=ft.Row([
                                                ft.Column([
                                                    ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                    ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                    ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                    ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                    ], spacing=1),
                                                # ft.Icon(ft.Icons.PERSON)
                                                ft.IconButton(
                                                    ft.Icons.PERSON,
                                                    # icon_color=ft.Colors.BLUE_700,
                                                    tooltip="Mudar Senha Usuário",
                                                    on_click=lambda _: page.go("/mudarsenha")
                                                    )
                                            ], 
                                            spacing=2,
                                            ),
                                            padding=ft.padding.only(right=20)
                                        )
                                    ],
                                  leading=ft.IconButton(
                                      icon=ft.Icons.ARROW_BACK,
                                      tooltip="Voltar",  # Tooltip modificado
                                      on_click=lambda _: page.go("/menu"),  # Comportamento de voltar padrão
                                    ),
                                ),
                            ft.Row(
                                    controls=[ft.ElevatedButton("Criar Material Educativo", style=button_style, disabled=not flag_permissao, on_click=lambda _: page.go("/criarmaterial"), icon=ft.Icons.ADD_SHARP)],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        tabela,
                                        expand=True,
                                        border_radius=0,
                                    ),
                                ],
                                expand=True,
                            )
                        ],
                    )
                )

            # Página Visualizar Material Educativo
            if page.route == "/material":
                material = bd.buscar_material_educativo_por_id(w_material_id)
                usuario = bd.buscar_usuario_por_id(material["UsuarioIdCriou"]) # type: ignore
                aux_usuario_criou = f"{material['UsuarioIdCriou']}" # type: ignore
                if not usuario == None:
                    aux_usuario_criou = f"{material['UsuarioIdCriou']} - {usuario['Nome']}" # type: ignore
                aux_usuario_alterou = " "
                if not material['UsuarioIdAlterou'] == 0:  # type: ignore   
                   aux_usuario_alterou = f"{material['UsuarioIdAlterou']}" # type: ignore
                   if not usuario == None:
                      aux_usuario_alterou = f"{material['UsuarioIdAlterou']} - {usuario['Nome']}" # type: ignore
                tf_v_id_material = ft.TextField(label="Id", value=str(w_material_id), read_only=True)
                tf_v_descricao_material = ft.TextField(label="Descrição", value=material["Descricao"], read_only=True, width=610, max_lines=3) # type: ignore
                tf_v_link_material = ft.TextField(label="Link", value=material["Link"], read_only=True, multiline=True, width=610, max_lines=3) # type: ignore
                tf_v_usuario_criou_material = ft.TextField(label="Usuário Criou", value=aux_usuario_criou, read_only=True, multiline=True, width=610, max_lines=3) # type: ignore
                tf_v_usuario_alterou_material = ft.TextField(label="Usuário Alterou", value=aux_usuario_alterou, read_only=True, multiline=True, width=610, max_lines=3) # type: ignore
                tf_v_data_hora_ultima_material = ft.TextField(label="Data e Hora Última Alteração", value=datetime.fromisoformat(material["DataHoraUltAlt"]).strftime(FORMATO_DATA_HORA), read_only=True, width=200) # type: ignore
                cor = ft.Colors.BLACK
                if material["Status"] == "Ativo": # type: ignore
                    cor = ft.Colors.GREEN
                elif material["Status"] == "Não Ativo": # type: ignore
                    cor = ft.Colors.RED
                tf_v_status_material = ft.TextField(label="Status", value=material["Status"], read_only=True, color=cor) # type: ignore

                page.views.append(
                   ft.View(
                        "/material",
                        [
                            ft.AppBar(
                                title=ft.Text("Visualiza Material Educativo"),
                                color=ft.Colors.BLACK, 
                                bgcolor="#2E9239",
                                actions=[
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Column([
                                                ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                ], spacing=1),
                                            # ft.Icon(ft.Icons.PERSON)
                                            ft.IconButton(
                                                ft.Icons.PERSON,
                                                # icon_color=ft.Colors.BLUE_700,
                                                tooltip="Mudar Senha Usuário",
                                                on_click=lambda _: page.go("/mudarsenha")
                                                )
                                        ], 
                                        spacing=2,
                                        ),
                                        padding=ft.padding.only(right=20)
                                    )
                                ],
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/cadastromateriais"),  # Comportamento de voltar padrão
                                ),
                            ),
                            # ft.Container(content=ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, controls=[
                                ft.Row(
                                    controls=[tf_v_id_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_descricao_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_link_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_usuario_criou_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_usuario_alterou_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_data_hora_ultima_material, tf_v_status_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                            # ]), expand=True, padding=10),
                        ],
                    )
                )

            # Página Criar Material Educativo
            if page.route == "/criarmaterial":
                descricao_material_valida = False
                link_material_valida = False
                tf_descricao_material = ft.TextField(label="Descrição", multiline=True, width=610, max_lines=3, on_change=validar_descricao_material)  # type: ignore
                tf_link_material = ft.TextField(label="Link", multiline=True, width=610, max_lines=3, on_change=validar_link_material)  # type: ignore
                lb_erro_material = ft.Text("", color=ft.Colors.RED)
                bt_criar_material = ft.ElevatedButton("Salvar", style=button_style, on_click=criar_material, icon=ft.Icons.SAVE_ALT_SHARP, disabled=True)

                page.views.append(
                   ft.View(
                        "/criarmaterial",
                        [
                            ft.AppBar(
                                title=ft.Text("Criar Material Educativo"),
                                color=ft.Colors.BLACK, 
                                bgcolor="#2E9239",
                                actions=[
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Column([
                                                ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                ], spacing=1),
                                            # ft.Icon(ft.Icons.PERSON)
                                            ft.IconButton(
                                                ft.Icons.PERSON,
                                                # icon_color=ft.Colors.BLUE_700,
                                                tooltip="Mudar Senha Usuário",
                                                on_click=lambda _: page.go("/mudarsenha")
                                                )
                                        ], 
                                        spacing=2,
                                        ),
                                        padding=ft.padding.only(right=20)
                                    )
                                ],
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/cadastromateriais"),  # Comportamento de voltar padrão
                                ),
                            ),
                            # ft.Container(content=ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, controls=[
                                ft.Row(
                                    controls=[tf_descricao_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_link_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[lb_erro_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[bt_criar_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                            # ]), expand=True, padding=10),
                        ],
                    )
                )

            # Página Editar Material Educativo
            if page.route == "/editarmaterial":
                descricao_material_valida = True
                link_material_valida = True
                status_material_valida = True
                material = bd.buscar_material_educativo_por_id(w_material_id)
                tf_v_id_material = ft.TextField(label="Id", value=str(w_material_id), read_only=True)
                tf_descricao_material = ft.TextField(label="Descrição", value=material["Descricao"], multiline=True, width=610, max_lines=3, on_change=validar_descricao_material_e)  # type: ignore
                tf_link_material = ft.TextField(label="Link", value=material["Link"], multiline=True, width=610, max_lines=3, on_change=validar_link_material_e)  # type: ignore
                dd_status_material = ft.Dropdown(label="Status", 
                                      options=[
                                          ft.dropdown.Option("Ativo"),
                                          ft.dropdown.Option("Não Ativo"),
                                          ], 
                                      value=material["Status"],   # type: ignore
                                      on_change=validar_status_material_e)
                lb_erro_material = ft.Text("", color=ft.Colors.RED)
                bt_editar_material = ft.ElevatedButton("Salvar", style=button_style, on_click=editar_material, icon=ft.Icons.SAVE_ALT_SHARP, disabled=True)

                page.views.append(
                   ft.View(
                        "/editarmaterial",
                        [
                            ft.AppBar(
                                title=ft.Text("Editar Material Educativo"),
                                color=ft.Colors.BLACK, 
                                bgcolor="#2E9239",
                                actions=[
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Column([
                                                ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                ], spacing=1),
                                            # ft.Icon(ft.Icons.PERSON)
                                            ft.IconButton(
                                                ft.Icons.PERSON,
                                                # icon_color=ft.Colors.BLUE_700,
                                                tooltip="Mudar Senha Usuário",
                                                on_click=lambda _: page.go("/mudarsenha")
                                                )
                                        ], 
                                        spacing=2,
                                        ),
                                        padding=ft.padding.only(right=20)
                                    )
                                ],
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/cadastromateriais"),  # Comportamento de voltar padrão
                                ),
                            ),
                            # ft.Container(content=ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, controls=[

                                ft.Row(
                                    controls=[tf_v_id_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_descricao_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_link_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[dd_status_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[lb_erro_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[bt_editar_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                            # ]), expand=True, padding=10),
                        ],
                    )
                )

            # Página Apagar material Educativo
            if page.route == "/apagarmaterial":
                material = bd.buscar_material_educativo_por_id(w_material_id)
                usuario = bd.buscar_usuario_por_id(material["UsuarioIdCriou"]) # type: ignore
                aux_usuario_criou = f"{material['UsuarioIdCriou']}" # type: ignore
                if not usuario == None:
                    aux_usuario_criou = f"{material['UsuarioIdCriou']} - {usuario['Nome']}" # type: ignore
                aux_usuario_alterou = " "
                if not material['UsuarioIdAlterou'] == 0:  # type: ignore   
                   aux_usuario_alterou = f"{material['UsuarioIdAlterou']}" # type: ignore
                   if not usuario == None:
                      aux_usuario_alterou = f"{material['UsuarioIdAlterou']} - {usuario['Nome']}" # type: ignore
                tf_v_id_material = ft.TextField(label="Id", value=str(w_material_id), read_only=True)
                tf_v_descricao_material = ft.TextField(label="Descrição", value=material["Descricao"], read_only=True, width=610, max_lines=3) # type: ignore
                tf_v_link_material = ft.TextField(label="Link", value=material["Link"], read_only=True, multiline=True, width=610, max_lines=3) # type: ignore
                tf_v_usuario_criou_material = ft.TextField(label="Usuário Criou", value=aux_usuario_criou, read_only=True, multiline=True, width=610, max_lines=3) # type: ignore
                tf_v_usuario_alterou_material = ft.TextField(label="Usuário Alterou", value=aux_usuario_alterou, read_only=True, multiline=True, width=610, max_lines=3) # type: ignore
                tf_v_data_hora_ultima_material = ft.TextField(label="Data e Hora Última Alteração", value=datetime.fromisoformat(material["DataHoraUltAlt"]).strftime(FORMATO_DATA_HORA), read_only=True, width=200) # type: ignore
                cor = ft.Colors.BLACK
                if material["Status"] == "Ativo": # type: ignore
                    cor = ft.Colors.GREEN
                elif material["Status"] == "Não Ativo": # type: ignore
                    cor = ft.Colors.RED
                tf_v_status_material = ft.TextField(label="Status", value=material["Status"], read_only=True, color=cor) # type: ignore
                bt_apagar_material = ft.ElevatedButton("Apagar", style=button_style, on_click=apagar_material, icon=ft.Icons.DELETE)

                page.views.append(
                   ft.View(
                        "/apagarmaterial",
                        [
                            ft.AppBar(
                                title=ft.Text("Apagar Material Educativo"),
                                color=ft.Colors.BLACK, 
                                bgcolor="#2E9239",
                                actions=[
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Column([
                                                ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                ], spacing=1),
                                            # ft.Icon(ft.Icons.PERSON)
                                            ft.IconButton(
                                                ft.Icons.PERSON,
                                                # icon_color=ft.Colors.BLUE_700,
                                                tooltip="Mudar Senha Usuário",
                                                on_click=lambda _: page.go("/mudarsenha")
                                                )
                                        ], 
                                        spacing=2,
                                        ),
                                        padding=ft.padding.only(right=20)
                                    )
                                ],
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/cadastromateriais"),  # Comportamento de voltar padrão
                                ),
                            ),
                            # ft.Container(content=ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, controls=[
                                ft.Row(
                                    controls=[tf_v_id_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_descricao_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_link_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_usuario_criou_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_usuario_alterou_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_data_hora_ultima_material, tf_v_status_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[ft.Text("Apagar o Material Educativo?", weight=ft.FontWeight.BOLD, color=ft.Colors.RED)],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[bt_apagar_material],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                            # ]), expand=True, padding=10),
                        ],
                    )
                )

            # Página Visualizar Log
            if page.route == "/visualizarlog":
                flag_permissao = True
                # Cabeçalho fixo
                cabecalho = ft.Row(
                    controls=[
                        criar_celula(ft.Text("Id", weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                        criar_celula(ft.Text("Data e Hora", weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                        criar_celula(ft.Text("Descrição", weight=ft.FontWeight.BOLD), 650, ft.alignment.top_center),
                        criar_celula(ft.Text("Usuário", weight=ft.FontWeight.BOLD), 300, ft.alignment.top_center),
                    ],
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.START
                )
                logs = bd.listar_log()
                # Corpo da tabela com scroll
                linhas = []
                zebrado = False
                for loga in logs:
                    if zebrado:
                        cor_zebrado = "#D4F1C1"
                    else:
                        cor_zebrado = ft.Colors.WHITE
                    zebrado = not zebrado
                    data_obj = datetime.strptime(loga["DataHora"], FORMATO_DATA_HORA_ISO)
                    data_formatada = data_obj.strftime(FORMATO_DATA_HORA)
                    usuario = bd.buscar_usuario_por_id(loga["Usuarioid"]) # type: ignore
                    aux_usuario_log = f"{loga['Usuarioid']}" # type: ignore
                    if not usuario == None:
                       aux_usuario_log = f"{loga['Usuarioid']} - {usuario['Nome']}" # type: ignore
                    linhas.append(
                        ft.Container(
                            ft.Row(
                                controls=[
                                    criar_celula(ft.Text(loga["LoglId"], weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                                    criar_celula(ft.Text(data_formatada, weight=ft.FontWeight.BOLD), 150, ft.alignment.top_center),
                                    criar_celula(
                                        ft.Text(
                                            loga["Descricao"],
                                            max_lines=3,
                                            overflow=ft.TextOverflow.ELLIPSIS,
                                            tooltip=loga["Descricao"],
                                            selectable=True,
                                        ), 
                                        650
                                    ),
                                    criar_celula(ft.Text(aux_usuario_log, weight=ft.FontWeight.BOLD), 300, ft.alignment.top_center),
                                ],
                                spacing=0,
                                vertical_alignment=ft.CrossAxisAlignment.START
                            ),
                            bgcolor=cor_zebrado,
                            padding=0,
                            border=ft.border.only(
                                top=ft.border.BorderSide(1, "#D4F1C1"),
                                # left=ft.border.BorderSide(1, "#D4F1C1"),
                                # right=ft.border.BorderSide(1, "#D4F1C1")
                            )
                        )
                    )
                # Tabela completa
                tabela = ft.Column(
                    controls=[
                        # Cabeçalho fixo
                        ft.Container(
                            cabecalho,
                            bgcolor="#8CDF7C",
                            padding=10,
                            border=ft.border.only(
                                top=ft.border.BorderSide(1, "#D4F1C1"),
                                left=ft.border.BorderSide(1, "#D4F1C1"),
                                right=ft.border.BorderSide(1, "#D4F1C1")
                            )
                        ),
                        # Corpo com scroll
                        ft.Container(
                            content=ft.ListView(
                                controls=linhas,
                                expand=True,
                                spacing=0,
                                padding=0,
                            ),
                            border=ft.border.only(
                                bottom=ft.border.BorderSide(1, ft.Colors.BLUE_400),
                                left=ft.border.BorderSide(1, ft.Colors.BLUE_400),
                                right=ft.border.BorderSide(1, ft.Colors.BLUE_400)
                            ),
                            expand=True
                        )
                    ],
                    spacing=0,
                    expand=True
                )
                page.views.append(
                   ft.View(
                        "/visualizarlog",
                        [
                            ft.AppBar(title=ft.Text(f"Visualizar Log"), 
                                    color=ft.Colors.BLACK, 
                                    bgcolor="#2E9239",
                                    center_title=False,
                                    actions=[
                                        ft.Container(
                                            content=ft.Row([
                                                ft.Column([
                                                    ft.Text(f"Id: {usuario_id}", size=10, height=13),
                                                    ft.Text(f"Nome: {usuario_nome}", size=10, height=13),
                                                    ft.Text(f"Email: {usuario_email}", size=10, height=13),
                                                    ft.Text(f"Tipo: {usuario_tipo}", size=10, height=13),
                                                    ], spacing=1),
                                                # ft.Icon(ft.Icons.PERSON)
                                                ft.IconButton(
                                                    ft.Icons.PERSON,
                                                    # icon_color=ft.Colors.BLUE_700,
                                                    tooltip="Mudar Senha Usuário",
                                                    on_click=lambda _: page.go("/mudarsenha")
                                                    )
                                            ], 
                                            spacing=2,
                                            ),
                                            padding=ft.padding.only(right=20)
                                        )
                                    ],
                                  leading=ft.IconButton(
                                      icon=ft.Icons.ARROW_BACK,
                                      tooltip="Voltar",  # Tooltip modificado
                                      on_click=lambda _: page.go("/menu"),  # Comportamento de voltar padrão
                                    ),
                                ),
                            # ft.Row(
                            #         controls=[ft.ElevatedButton("Filtro", on_click=lambda _: page.go("/menu"), icon=ft.Icons.FILTER_ALT)],
                            #         alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            # ),
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        tabela,
                                        expand=True,
                                        border_radius=0,
                                    ),
                                ],
                                expand=True,
                            )
                        ],
                    )
                )


            page.update()

        # Fechar a view atual e voltar à anterior
        def view_pop(e):
            page.views.pop()
            top_view = page.views[-1]
            if top_view.route:
                page.go(top_view.route)

        # Atribui Eventos
        page.on_route_change = route_change
        page.on_view_pop = view_pop

        page.go(page.route)

    except Exception as e:
        print(f"Erro: {e}")

# Início da Aplicação
if __name__ == '__main__':
    ft.app(target=main)
