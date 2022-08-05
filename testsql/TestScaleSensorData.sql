USE [fyp-kitchencontrol-db]
GO

INSERT INTO [dbo].[scale_history]
           ([reading_datetime],[iot_device_id],[weight])
     VALUES
			(CAST(N'2022-02-26 02:03:03.000' AS DateTime),25,25),
			(CAST(N'2022-02-26 02:03:13.000' AS DateTime),25,24.5),
			(CAST(N'2022-02-26 02:03:23.000' AS DateTime),25,24),
			(CAST(N'2022-02-26 02:03:33.000' AS DateTime),25,23.5),
			(CAST(N'2022-02-26 02:03:43.000' AS DateTime),25,23),
			(CAST(N'2022-02-26 02:03:53.000' AS DateTime),25,22.5),
			(CAST(N'2022-02-26 02:04:03.000' AS DateTime),25,22),
			(CAST(N'2022-02-26 02:04:13.000' AS DateTime),25,21.5),
			(CAST(N'2022-02-26 02:04:23.000' AS DateTime),25,21),
			(CAST(N'2022-02-26 02:04:33.000' AS DateTime),25,20.5),
			(CAST(N'2022-02-26 02:04:43.000' AS DateTime),25,20),
			(CAST(N'2022-02-26 02:04:53.000' AS DateTime),25,19.5),
			(CAST(N'2022-02-26 02:05:03.000' AS DateTime),25,19),
			(CAST(N'2022-02-26 02:05:13.000' AS DateTime),25,25),
			(CAST(N'2022-02-26 02:05:23.000' AS DateTime),25,24.5),
			(CAST(N'2022-02-26 02:05:33.000' AS DateTime),25,24),
			(CAST(N'2022-02-26 02:05:43.000' AS DateTime),25,23.5),
			(CAST(N'2022-02-26 02:05:53.000' AS DateTime),25,23),
			(CAST(N'2022-02-26 02:06:03.000' AS DateTime),25,22.5),
			(CAST(N'2022-02-26 02:06:13.000' AS DateTime),25,22),
			(CAST(N'2022-02-26 02:06:23.000' AS DateTime),25,21.5),
			(CAST(N'2022-02-26 02:06:33.000' AS DateTime),25,21),
			(CAST(N'2022-02-26 02:06:43.000' AS DateTime),25,20.5),

			(CAST(N'2022-02-26 02:03:03.000' AS DateTime),26,25),
			(CAST(N'2022-02-26 02:03:13.000' AS DateTime),26,24.5),
			(CAST(N'2022-02-26 02:03:23.000' AS DateTime),26,24),
			(CAST(N'2022-02-26 02:03:33.000' AS DateTime),26,23.5),
			(CAST(N'2022-02-26 02:03:43.000' AS DateTime),26,23),
			(CAST(N'2022-02-26 02:03:53.000' AS DateTime),26,22.5),
			(CAST(N'2022-02-26 02:04:03.000' AS DateTime),26,22),
			(CAST(N'2022-02-26 02:04:13.000' AS DateTime),26,21.5),
			(CAST(N'2022-02-26 02:04:23.000' AS DateTime),26,21),
			(CAST(N'2022-02-26 02:04:33.000' AS DateTime),26,20.5),
			(CAST(N'2022-02-26 02:04:43.000' AS DateTime),26,20),
			(CAST(N'2022-02-26 02:04:53.000' AS DateTime),26,19.5),
			(CAST(N'2022-02-26 02:05:03.000' AS DateTime),26,19),
			(CAST(N'2022-02-26 02:05:13.000' AS DateTime),26,25),
			(CAST(N'2022-02-26 02:05:23.000' AS DateTime),26,24.5),
			(CAST(N'2022-02-26 02:05:33.000' AS DateTime),26,24),
			(CAST(N'2022-02-26 02:05:43.000' AS DateTime),26,23.5),
			(CAST(N'2022-02-26 02:05:53.000' AS DateTime),26,23),
			(CAST(N'2022-02-26 02:06:03.000' AS DateTime),26,22.5),
			(CAST(N'2022-02-26 02:06:13.000' AS DateTime),26,22),
			(CAST(N'2022-02-26 02:06:23.000' AS DateTime),26,21.5),
			(CAST(N'2022-02-26 02:06:33.000' AS DateTime),26,21),
			(CAST(N'2022-02-26 02:06:43.000' AS DateTime),26,20.5),

			(CAST(N'2022-02-26 02:03:03.000' AS DateTime),27,25),
			(CAST(N'2022-02-26 02:03:13.000' AS DateTime),27,24.5),
			(CAST(N'2022-02-26 02:03:23.000' AS DateTime),27,24),
			(CAST(N'2022-02-26 02:03:33.000' AS DateTime),27,23.5),
			(CAST(N'2022-02-26 02:03:43.000' AS DateTime),27,23),
			(CAST(N'2022-02-26 02:03:53.000' AS DateTime),27,22.5),
			(CAST(N'2022-02-26 02:04:03.000' AS DateTime),27,22),
			(CAST(N'2022-02-26 02:04:13.000' AS DateTime),27,21.5),
			(CAST(N'2022-02-26 02:04:23.000' AS DateTime),27,21),
			(CAST(N'2022-02-26 02:04:33.000' AS DateTime),27,20.5),
			(CAST(N'2022-02-26 02:04:43.000' AS DateTime),27,20),
			(CAST(N'2022-02-26 02:04:53.000' AS DateTime),27,19.5),
			(CAST(N'2022-02-26 02:05:03.000' AS DateTime),27,19),
			(CAST(N'2022-02-26 02:05:13.000' AS DateTime),27,25),
			(CAST(N'2022-02-26 02:05:23.000' AS DateTime),27,24.5),
			(CAST(N'2022-02-26 02:05:33.000' AS DateTime),27,24),
			(CAST(N'2022-02-26 02:05:43.000' AS DateTime),27,23.5),
			(CAST(N'2022-02-26 02:05:53.000' AS DateTime),27,23),
			(CAST(N'2022-02-26 02:06:03.000' AS DateTime),27,22.5),
			(CAST(N'2022-02-26 02:06:13.000' AS DateTime),27,22),
			(CAST(N'2022-02-26 02:06:23.000' AS DateTime),27,21.5),
			(CAST(N'2022-02-26 02:06:33.000' AS DateTime),27,21),
			(CAST(N'2022-02-26 02:06:43.000' AS DateTime),27,20.5),

			(CAST(N'2022-02-26 02:03:03.000' AS DateTime),28,25),
			(CAST(N'2022-02-26 02:03:13.000' AS DateTime),28,24.5),
			(CAST(N'2022-02-26 02:03:23.000' AS DateTime),28,24),
			(CAST(N'2022-02-26 02:03:33.000' AS DateTime),28,23.5),
			(CAST(N'2022-02-26 02:03:43.000' AS DateTime),28,23),
			(CAST(N'2022-02-26 02:03:53.000' AS DateTime),28,22.5),
			(CAST(N'2022-02-26 02:04:03.000' AS DateTime),28,22),
			(CAST(N'2022-02-26 02:04:13.000' AS DateTime),28,21.5),
			(CAST(N'2022-02-26 02:04:23.000' AS DateTime),28,21),
			(CAST(N'2022-02-26 02:04:33.000' AS DateTime),28,20.5),
			(CAST(N'2022-02-26 02:04:43.000' AS DateTime),28,20),
			(CAST(N'2022-02-26 02:04:53.000' AS DateTime),28,19.5),
			(CAST(N'2022-02-26 02:05:03.000' AS DateTime),28,19),
			(CAST(N'2022-02-26 02:05:13.000' AS DateTime),28,25),
			(CAST(N'2022-02-26 02:05:23.000' AS DateTime),28,24.5),
			(CAST(N'2022-02-26 02:05:33.000' AS DateTime),28,24),
			(CAST(N'2022-02-26 02:05:43.000' AS DateTime),28,23.5),
			(CAST(N'2022-02-26 02:05:53.000' AS DateTime),28,23),
			(CAST(N'2022-02-26 02:06:03.000' AS DateTime),28,22.5),
			(CAST(N'2022-02-26 02:06:13.000' AS DateTime),28,22),
			(CAST(N'2022-02-26 02:06:23.000' AS DateTime),28,21.5),
			(CAST(N'2022-02-26 02:06:33.000' AS DateTime),28,21),
			(CAST(N'2022-02-26 02:06:43.000' AS DateTime),28,20.5),

			(CAST(N'2022-02-26 02:03:03.000' AS DateTime),29,25),
			(CAST(N'2022-02-26 02:03:13.000' AS DateTime),29,24.5),
			(CAST(N'2022-02-26 02:03:23.000' AS DateTime),29,24),
			(CAST(N'2022-02-26 02:03:33.000' AS DateTime),29,23.5),
			(CAST(N'2022-02-26 02:03:43.000' AS DateTime),29,23),
			(CAST(N'2022-02-26 02:03:53.000' AS DateTime),29,22.5),
			(CAST(N'2022-02-26 02:04:03.000' AS DateTime),29,22),
			(CAST(N'2022-02-26 02:04:13.000' AS DateTime),29,21.5),
			(CAST(N'2022-02-26 02:04:23.000' AS DateTime),29,21),
			(CAST(N'2022-02-26 02:04:33.000' AS DateTime),29,20.5),
			(CAST(N'2022-02-26 02:04:43.000' AS DateTime),29,20),
			(CAST(N'2022-02-26 02:04:53.000' AS DateTime),29,19.5),
			(CAST(N'2022-02-26 02:05:03.000' AS DateTime),29,19),
			(CAST(N'2022-02-26 02:05:13.000' AS DateTime),29,25),
			(CAST(N'2022-02-26 02:05:23.000' AS DateTime),29,24.5),
			(CAST(N'2022-02-26 02:05:33.000' AS DateTime),29,24),
			(CAST(N'2022-02-26 02:05:43.000' AS DateTime),29,23.5),
			(CAST(N'2022-02-26 02:05:53.000' AS DateTime),29,23),
			(CAST(N'2022-02-26 02:06:03.000' AS DateTime),29,22.5),
			(CAST(N'2022-02-26 02:06:13.000' AS DateTime),29,22),
			(CAST(N'2022-02-26 02:06:23.000' AS DateTime),29,21.5),
			(CAST(N'2022-02-26 02:06:33.000' AS DateTime),29,21),
			(CAST(N'2022-02-26 02:06:43.000' AS DateTime),29,20.5)

GO
