import flet as ft
import os
import time
import datetime
def main(page: ft.Page):
    page.title = "Dear Diary | Flet"
    page.theme_mode = ft.ThemeMode.LIGHT

    def changetheme(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if darklight.value else ft.ThemeMode.LIGHT
        )
        page.update()

    darklight = ft.Switch(label="🌞/🌙", value=False, on_change=changetheme)
    

    _ = ft.Text(
        "📔 Welcome to Alejuaniel's Diary Simulator!\nFollow the instructions below.",
        font_family="Times New Roman",
        size=20,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )

    def seepassword(e):
        passwordQuestion2.password = not passwordQuestion2.password
        showpassword.icon = (
            ft.icons.VISIBILITY if not passwordQuestion2.password else ft.icons.VISIBILITY_OFF
        )
        showpassword.tooltip = (
            "Hide password" if not passwordQuestion2.password else "Show password"
        )
        page.update()

    showpassword = ft.IconButton(
        icon=ft.icons.VISIBILITY_OFF,
        tooltip="Show password",
        on_click=seepassword
    )

    passwordQuestion2 = ft.TextField(
        label="Password field",
        visible=False,
        password=True,
        can_reveal_password=False,
        suffix=showpassword
    )

    

    def newpassword(e):
        with open("password.txt", "w", encoding="UTF-8") as file:
            file.write(passwordQuestion2.value)
        passwordQuestion2.visible = False
        confirmPassword2.visible = False
        addtextButton.visible = True
        seediarybutton.visible = True
        deleteentrysbutton.visible = True
        exitButton.visible = True
        page.update()

    def confirmPassworddef(e):
        with open("password.txt", "r") as file:
            passwordConfirm2 = file.read()

        if passwordConfirm2 == passwordQuestion2.value:
            _.visible = False
            passwordQuestion2.visible = False
            confirmPassword.visible = False
            addtextButton.visible = True
            seediarybutton.visible = True
            deleteentrysbutton.visible = True
            exitButton.visible = True
        else:
            passwordQuestion2.label = "❌ Incorrect password, locked for 5 seconds."
            passwordQuestion2.read_only = True
            page.update()
            time.sleep(5)
            passwordQuestion2.read_only = False
            passwordQuestion2.label = "Input your password here."

        page.update()

    def newentry(e):
        hide(e)
        entrytextfield.visible = True
        submitentrybutton.visible = True
        backbutton.visible = True
        page.update()

    def show(e):
        addtextButton.visible = True
        deleteentrysbutton.visible = True
        seediarybutton.visible = True
        exitButton.visible = True
        page.update()

    def addentry(e):
        if entrytextfield.value != "":
            x = datetime.datetime.now()
            with open("alejuanieldiary", "a", encoding="UTF-8") as file:
                file.write(f"Date: {x.strftime("%x")} Time: {x.strftime("%X")}| {entrytextfield.value}\n")

        entrytextfield.visible = False
        submitentrybutton.visible = False
        entrytextfield.value = ""
        show(e)
        page.update()

    def seediary(e):
        hide(e)
        if os.path.exists("alejuanieldiary"):
            with open("alejuanieldiary", "r", encoding="UTF-8") as file:
                diarytext = file.read()
        else:
            diarytext = "No entries yet."

        diarytextflet.value = diarytext
        diarytextflet.visible = True
        backbutton.visible = True
        page.update()

    def back(e):
        diarytextflet.visible = False
        backbutton.visible = False
        deleteinfo.visible = False
        entrynumbertextfield.visible = False
        confirmdeletebutton.visible = False
        submitentrybutton.visible = False
        entrytextfield.visible = False
        show(e)
        page.update()

    def deleteentrys(e):
        hide(e)
        backbutton.visible = True
        if os.path.exists("alejuanieldiary"):
            with open("alejuanieldiary", "r", encoding="UTF-8") as file:
                lines = file.readlines()
        else:
            deleteinfo.value = "No entries to delete."
            deleteinfo.visible = True
            page.update()
            return

        if lines:
            numberLine = ""
            for i in range(len(lines)):
                numberLine += f"{i+1}. {lines[i]}"
            deleteinfo.value = numberLine
        else:
            deleteinfo.value = "No entries to delete."
        deleteinfo.visible = True
        entrynumbertextfield.visible = True
        confirmdeletebutton.visible = True
        page.update()

    def hide(e):
        addtextButton.visible = False
        seediarybutton.visible = False
        deleteentrysbutton.visible = False
        exitButton.visible = False
        page.update()

    def confirmdelete(e):
        try:
            index = int(entrynumbertextfield.value) - 1
            with open("alejuanieldiary", "r", encoding="UTF-8") as file:
                lines = file.readlines()
            if 0 <= index < len(lines):
                lines.pop(index)
                with open("alejuanieldiary", "w", encoding="UTF-8") as file:
                    file.writelines(lines)
                deleteinfo.value = "✅ Entry deleted successfully."
                page.update()
                time.sleep(1.5)
                back(e)
            else:
                deleteinfo.value = "⚠️ Invalid entry number."
        except ValueError:
            deleteinfo.value = "❗ Please enter a valid number."

        entrynumbertextfield.value = ""
        page.update()

    def exit(e):
        page.window.close()

    confirmPassword = ft.ElevatedButton("🔒 Confirm here.", visible=False, on_click=confirmPassworddef)
    confirmPassword2 = ft.ElevatedButton("✅ Confirm here.", visible=False, on_click=newpassword)

    addtextButton = ft.ElevatedButton("📝 New entry to your diary", visible=False, on_click=newentry)
    seediarybutton = ft.ElevatedButton("📖 See your diary", visible=False, on_click= seediary)
    deleteentrysbutton = ft.ElevatedButton("🗑️ Delete entries", visible=False, on_click=deleteentrys)
    exitButton = ft.ElevatedButton("🚪 Exit", visible=False, on_click=exit)

    entrytextfield = ft.TextField(label="Your diary entry", visible=False, multiline=True, width=400, height=100)
    submitentrybutton = ft.ElevatedButton("📤 Submit", visible=False, on_click=addentry)

    diarytextflet = ft.Text("", visible=False)
    backbutton = ft.ElevatedButton("🔙 Back", visible=False, on_click=back)

    deleteinfo = ft.Text("", visible=False)
    entrynumbertextfield = ft.TextField(label="Number of entry to delete", visible=False)
    confirmdeletebutton = ft.ElevatedButton("🗑️ Delete", visible=False, on_click=confirmdelete)

    if os.path.exists("password.txt"):
        passwordQuestion2.label = "Input your password here."
        passwordQuestion2.visible = True
        confirmPassword.visible = True
    else:
        passwordQuestion2.label = "Create a new password."
        passwordQuestion2.visible = True
        confirmPassword2.visible = True

    button_row = ft.Row(
        controls=[
            addtextButton,
            seediarybutton,
            deleteentrysbutton,
            exitButton
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    )

    entry_controls = ft.Column(
        controls=[
            entrytextfield,
            submitentrybutton
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    delete_controls = ft.Column(
        controls=[
            deleteinfo,
            entrynumbertextfield,
            confirmdeletebutton
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(
        ft.Row([darklight], alignment=ft.MainAxisAlignment.END),
        ft.Container(content=_, alignment=ft.alignment.center, padding=20),
        passwordQuestion2,
        confirmPassword,
        confirmPassword2,
        button_row,
        entry_controls,
        diarytextflet,
        delete_controls,
        backbutton
    )

    page.update()

ft.app(target=main)
