from jnius import autoclass
import os

class FletNotification:
    def send(self, title, text, channel_id: str, channel_name: str):
        # Get the main activity from the environment
        activity_host_class = os.getenv("MAIN_ACTIVITY_HOST_CLASS_NAME")
        assert activity_host_class
        activity_host = autoclass(activity_host_class)
        activity = activity_host.mActivity

        # Access the Android notification manager
        Context = autoclass('android.content.Context')
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        Notification = autoclass('android.app.Notification')
        NotificationBuilder = autoclass('android.app.Notification$Builder')

        # Start the notification service
        notification_service = activity.getSystemService(Context.NOTIFICATION_SERVICE)

        # Create a notification channel (for Android 8.0 and above)
        channel_id = "my_notification_channel"
        channel_name = "Flet Notification Channel"
        importance = NotificationManager.IMPORTANCE_MAX

        # Create the notification channel (Android 8.0+)
        channel = NotificationChannel(channel_id, channel_name, importance)
        notification_service.createNotificationChannel(channel)

        # Build the notification
        builder = NotificationBuilder(activity, channel_id)
        builder.setContentTitle(title)
        builder.setContentText(text)
        builder.setSmallIcon(activity.getApplicationInfo().icon)
        builder.setAutoCancel(True)

        # Display the notification
        notification_id = 1
        notification = builder.build()
        notification_service.notify(notification_id, notification)