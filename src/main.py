from flet_post_notification import FletNotification
import flet_permission_handler as fph
from desktop_notifier import ReplyField
from desktop_notifier import Button as DesktopButton
from flet import *

def main(page: Page):
    page.title = "Notification Example"

    ph = fph.PermissionHandler()
    page.overlay.append(ph)

    notification = FletNotification(page)

    check_text = Text("Check Notification Permission Status: 'Unknow' ", color=Colors.GREY)
    request_text = Text("Request Notification Permission Status: 'Unknow' ", color=Colors.GREY)

    notify_button = ElevatedButton("Send Notification", disabled=True)

    async def on_notify_click(e):
        title = " Flet Notification"
        text = " This is a text Notification"
        await notification.send(
            title, 
            text, 
            "test-id", 
            "test-name",
            field=ReplyField("Reply", on_replied=lambda e: print(e)),
            actions=[
                DesktopButton("Action 1", on_pressed=lambda e: print("Action 1 clicked")),
                DesktopButton("Action 2", on_pressed=lambda e: print("Action 2 clicked")),
            ]
        )
        page.update()

    notify_button.on_click = on_notify_click

    def check_permission(e):
        result = ph.check_permission(e.control.data)
        check_text.value = f"Permission Check. {e.control.data.name} - {result}"
        notify_button.disabled = not result
        check_text.color = Colors.GREEN if result else Colors.RED
        page.update()

    def request_permission(e):
        result = ph.request_permission(e.control.data)
        request_text.value = f"Permission requested: {e.control.data.name} - {result}"
        notify_button.disabled = not result
        request_text.color = Colors.GREEN if result else Colors.RED
        page.update()

    page.appbar = AppBar(title=Text("Notification Permission Manager"))

    page.add(
        SafeArea(
            content=Column(
                controls=[
                    check_text,
                    request_text,
                    OutlinedButton(
                        "Check Notification Permission",
                        data=fph.PermissionType.NOTIFICATION,
                        on_click=check_permission,
                    ),
                    OutlinedButton(
                        "Request Notification Permission",
                        data=fph.PermissionType.NOTIFICATION,
                        on_click=request_permission,
                    ),
                    notify_button,
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        )
    )

app(main)