from desktop_notifier import DesktopNotifier, ReplyField, Urgency
import desktop_notifier as dn
from typing import Sequence, Union, Callable 
from flet import PagePlatform, Page, Text
from jnius import autoclass
import os

class FletNotification:
    def __init__(self, page: Page):
        self.page = page

        # Validate page parameter
        if not self.page:
            raise ValueError("Page is required")
        
        if self.page.platform == PagePlatform.ANDROID:
            self.request_permission()

    def request_permission(self):
        activity_host_class = os.getenv("MAIN_ACTIVITY_HOST_CLASS_NAME")
        activity = autoclass(activity_host_class).mActivity

        BuildVersion = autoclass('android.os.Build$VERSION')
        ManifestPermission = autoclass('android.Manifest$permission')
        
        ContextCompat = autoclass('androidx.core.content.ContextCompat')
        ActivityCompat = autoclass('androidx.core.app.ActivityCompat')
        PackageManager = autoclass('android.content.pm.PackageManager')

        if BuildVersion.SDK_INT >= 33:
            permission = ManifestPermission.POST_NOTIFICATIONS
            
            check = ContextCompat.checkSelfPermission(activity, permission)
            
            if check != PackageManager.PERMISSION_GRANTED:
                ActivityCompat.requestPermissions(activity, [permission], 101)
    
    async def send(
        self, 
        title, 
        text, 
        channel_id: str = "default",
        channel_name: str = "Default",
        importance: str = "critical",
        field: Union[ReplyField, None] = None,
        actions: Sequence[dn.Button] = ()
    ):
        if self.page.platform == PagePlatform.ANDROID:
            self._android(title, text, channel_id, channel_name, importance) # If the platform is android call the android notification function
        elif self.page.platform == PagePlatform.IOS:
            # TODO: Implement iOS notification
            pass
        elif (
            self.page.platform == PagePlatform.WINDOWS 
            or self.page.platform == PagePlatform.MACOS 
            or self.page.platform == PagePlatform.LINUX
        ): # If the platform is desktop call the desktop notification function
            await self._desktop(title, text, importance, field, actions)

    async def _desktop(
        self, 
        title, 
        text, 
        importance: str, 
        field: ReplyField = None,
        actions: Sequence[dn.Button] = (),
        on_dispatched: Callable[[], None] | None = None,
        on_clicked: Callable[[], None] | None = None,
        on_dismissed: Callable[[], None] | None = None,
    ):
        notifier = DesktopNotifier(app_name="Sample App")
        await notifier.send(
            title=title,
            message=text,
            urgency=Urgency.Critical if importance == "critical" else Urgency.Normal,
            buttons=actions,
            reply_field=field,
            on_dispatched=on_dispatched,
            on_clicked=on_clicked,
            on_dismissed=on_dismissed,
        )

    def _android(self, title, text, channel_id: str, channel_name: str, importance: str):
        activity_host_class = os.getenv("MAIN_ACTIVITY_HOST_CLASS_NAME")
        assert activity_host_class
        activity_host = autoclass(activity_host_class)
        activity = activity_host.mActivity

        Context = autoclass('android.content.Context')
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        
        Intent = autoclass('android.content.Intent')
        PendingIntent = autoclass('android.app.PendingIntent')

        notification_service = activity.getSystemService(Context.NOTIFICATION_SERVICE)
        importance_level = NotificationManager.IMPORTANCE_MAX if importance == "critical" else NotificationManager.IMPORTANCE_DEFAULT

        # Crear el canal
        channel = NotificationChannel(channel_id, channel_name, importance_level)
        notification_service.createNotificationChannel(channel)

        intent = Intent(activity, activity.getClass())
        intent.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)

        flags = 134217728 | 67108864 
        pending_intent = PendingIntent.getActivity(activity, 0, intent, flags)

        builder = NotificationBuilder(activity, channel_id)
        builder.setContentTitle(title)
        builder.setContentText(text)
        builder.setSmallIcon(activity.getApplicationInfo().icon)
        builder.setAutoCancel(True)
        builder.setContentIntent(pending_intent)

        notification_id = 1
        notification_service.notify(notification_id, builder.build())