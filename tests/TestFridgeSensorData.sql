USE [fyp-kitchencontrol-db]
GO

INSERT INTO [dbo].[fridge_temp_history]
			([reading_datetime],[iot_device_id],[tempC],[tempF])
     VALUES

	 (CAST(N'2022-02-26 02:02:43.000' AS DateTime),9,-14,6.8),
	(CAST(N'2022-02-26 02:02:53.000' AS DateTime),9,-11,12.2),
	(CAST(N'2022-02-26 02:03:03.000' AS DateTime),9,-8,17.6),
	(CAST(N'2022-02-26 02:03:13.000' AS DateTime),9,-11,12.2),
	(CAST(N'2022-02-26 02:03:23.000' AS DateTime),9,-12,10.4),
	(CAST(N'2022-02-26 02:03:33.000' AS DateTime),9,-5,23),
	(CAST(N'2022-02-26 02:03:43.000' AS DateTime),9,-13,8.6),
	(CAST(N'2022-02-26 02:03:53.000' AS DateTime),9,-7,19.4),
	(CAST(N'2022-02-26 02:04:03.000' AS DateTime),9,-8,17.6),
	(CAST(N'2022-02-26 02:04:13.000' AS DateTime),9,-11,12.2),
	(CAST(N'2022-02-26 02:04:23.000' AS DateTime),9,-11,12.2),
	(CAST(N'2022-02-26 02:04:33.000' AS DateTime),9,-15,5),
	(CAST(N'2022-02-26 02:04:43.000' AS DateTime),9,-5,23),
	(CAST(N'2022-02-26 02:04:53.000' AS DateTime),9,-11,12.2),
	(CAST(N'2022-02-26 02:05:03.000' AS DateTime),9,-9,15.8),
	(CAST(N'2022-02-26 02:05:13.000' AS DateTime),9,-11,12.2),
	(CAST(N'2022-02-26 02:05:23.000' AS DateTime),9,-7,19.4),
	(CAST(N'2022-02-26 02:05:33.000' AS DateTime),9,-12,10.4),
	(CAST(N'2022-02-26 02:05:43.000' AS DateTime),9,-14,6.8),
	(CAST(N'2022-02-26 02:05:53.000' AS DateTime),9,-13,8.6),
	(CAST(N'2022-02-26 02:06:03.000' AS DateTime),9,-15,5),
	(CAST(N'2022-02-26 02:06:13.000' AS DateTime),9,-8,17.6),
	(CAST(N'2022-02-26 02:06:23.000' AS DateTime),9,-13,8.6),
	(CAST(N'2022-02-26 02:06:33.000' AS DateTime),9,-10,14),
	(CAST(N'2022-02-26 02:06:43.000' AS DateTime),9,-5,23),

	(CAST(N'2022-02-26 02:02:43.000' AS DateTime),10,-11,12.2),
	(CAST(N'2022-02-26 02:02:53.000' AS DateTime),10,-15,5),
	(CAST(N'2022-02-26 02:03:03.000' AS DateTime),10,-13,8.6),
	(CAST(N'2022-02-26 02:03:13.000' AS DateTime),10,-14,6.8),
	(CAST(N'2022-02-26 02:03:23.000' AS DateTime),10,-15,5),
	(CAST(N'2022-02-26 02:03:33.000' AS DateTime),10,-15,5),
	(CAST(N'2022-02-26 02:03:43.000' AS DateTime),10,-13,8.6),
	(CAST(N'2022-02-26 02:03:53.000' AS DateTime),10,-8,17.6),
	(CAST(N'2022-02-26 02:04:03.000' AS DateTime),10,-12,10.4),
	(CAST(N'2022-02-26 02:04:13.000' AS DateTime),10,-10,14),
	(CAST(N'2022-02-26 02:04:23.000' AS DateTime),10,-15,5),
	(CAST(N'2022-02-26 02:04:33.000' AS DateTime),10,-6,21.2),
	(CAST(N'2022-02-26 02:04:43.000' AS DateTime),10,-11,12.2),
	(CAST(N'2022-02-26 02:04:53.000' AS DateTime),10,-15,5),
	(CAST(N'2022-02-26 02:05:03.000' AS DateTime),10,-7,19.4),
	(CAST(N'2022-02-26 02:05:13.000' AS DateTime),10,-6,21.2),
	(CAST(N'2022-02-26 02:05:23.000' AS DateTime),10,-12,10.4),
	(CAST(N'2022-02-26 02:05:33.000' AS DateTime),10,-14,6.8),
	(CAST(N'2022-02-26 02:05:43.000' AS DateTime),10,-13,8.6),
	(CAST(N'2022-02-26 02:05:53.000' AS DateTime),10,-9,15.8),
	(CAST(N'2022-02-26 02:06:03.000' AS DateTime),10,-5,23),
	(CAST(N'2022-02-26 02:06:13.000' AS DateTime),10,-5,23),
	(CAST(N'2022-02-26 02:06:23.000' AS DateTime),10,-9,15.8),
	(CAST(N'2022-02-26 02:06:33.000' AS DateTime),10,-11,12.2),
	(CAST(N'2022-02-26 02:06:43.000' AS DateTime),10,-13,8.6),

	(CAST(N'2022-02-26 02:02:43.000' AS DateTime),11,-11,12.2),
	(CAST(N'2022-02-26 02:02:53.000' AS DateTime),11,-6,21.2),
	(CAST(N'2022-02-26 02:03:03.000' AS DateTime),11,-15,5),
	(CAST(N'2022-02-26 02:03:13.000' AS DateTime),11,-7,19.4),
	(CAST(N'2022-02-26 02:03:23.000' AS DateTime),11,-5,23),
	(CAST(N'2022-02-26 02:03:33.000' AS DateTime),11,-13,8.6),
	(CAST(N'2022-02-26 02:03:43.000' AS DateTime),11,-7,19.4),
	(CAST(N'2022-02-26 02:03:53.000' AS DateTime),11,-9,15.8),
	(CAST(N'2022-02-26 02:04:03.000' AS DateTime),11,-8,17.6),
	(CAST(N'2022-02-26 02:04:13.000' AS DateTime),11,-8,17.6),
	(CAST(N'2022-02-26 02:04:23.000' AS DateTime),11,-13,8.6),
	(CAST(N'2022-02-26 02:04:33.000' AS DateTime),11,-10,14),
	(CAST(N'2022-02-26 02:04:43.000' AS DateTime),11,-6,21.2),
	(CAST(N'2022-02-26 02:04:53.000' AS DateTime),11,-8,17.6),
	(CAST(N'2022-02-26 02:05:03.000' AS DateTime),11,-12,10.4),
	(CAST(N'2022-02-26 02:05:13.000' AS DateTime),11,-12,10.4),
	(CAST(N'2022-02-26 02:05:23.000' AS DateTime),11,-11,12.2),
	(CAST(N'2022-02-26 02:05:33.000' AS DateTime),11,-11,12.2),
	(CAST(N'2022-02-26 02:05:43.000' AS DateTime),11,-9,15.8),
	(CAST(N'2022-02-26 02:05:53.000' AS DateTime),11,-10,14),
	(CAST(N'2022-02-26 02:06:03.000' AS DateTime),11,-12,10.4),
	(CAST(N'2022-02-26 02:06:13.000' AS DateTime),11,-8,17.6),
	(CAST(N'2022-02-26 02:06:23.000' AS DateTime),11,-9,15.8),
	(CAST(N'2022-02-26 02:06:33.000' AS DateTime),11,-6,21.2),
	(CAST(N'2022-02-26 02:06:43.000' AS DateTime),11,-8,17.6),

	(CAST(N'2022-02-26 02:02:43.000' AS DateTime),12,-6,21.2),
	(CAST(N'2022-02-26 02:02:53.000' AS DateTime),12,-9,15.8),
	(CAST(N'2022-02-26 02:03:03.000' AS DateTime),12,-6,21.2),
	(CAST(N'2022-02-26 02:03:13.000' AS DateTime),12,-8,17.6),
	(CAST(N'2022-02-26 02:03:23.000' AS DateTime),12,-13,8.6),
	(CAST(N'2022-02-26 02:03:33.000' AS DateTime),12,-10,14),
	(CAST(N'2022-02-26 02:03:43.000' AS DateTime),12,-10,14),
	(CAST(N'2022-02-26 02:03:53.000' AS DateTime),12,-11,12.2),
	(CAST(N'2022-02-26 02:04:03.000' AS DateTime),12,-7,19.4),
	(CAST(N'2022-02-26 02:04:13.000' AS DateTime),12,-6,21.2),
	(CAST(N'2022-02-26 02:04:23.000' AS DateTime),12,-15,5),
	(CAST(N'2022-02-26 02:04:33.000' AS DateTime),12,-12,10.4),
	(CAST(N'2022-02-26 02:04:43.000' AS DateTime),12,-6,21.2),
	(CAST(N'2022-02-26 02:04:53.000' AS DateTime),12,-15,5),
	(CAST(N'2022-02-26 02:05:03.000' AS DateTime),12,-12,10.4),
	(CAST(N'2022-02-26 02:05:13.000' AS DateTime),12,-7,19.4),
	(CAST(N'2022-02-26 02:05:23.000' AS DateTime),12,-10,14),
	(CAST(N'2022-02-26 02:05:33.000' AS DateTime),12,-6,21.2),
	(CAST(N'2022-02-26 02:05:43.000' AS DateTime),12,-14,6.8),
	(CAST(N'2022-02-26 02:05:53.000' AS DateTime),12,-6,21.2),
	(CAST(N'2022-02-26 02:06:03.000' AS DateTime),12,-13,8.6),
	(CAST(N'2022-02-26 02:06:13.000' AS DateTime),12,-14,6.8),
	(CAST(N'2022-02-26 02:06:23.000' AS DateTime),12,-11,12.2),
	(CAST(N'2022-02-26 02:06:33.000' AS DateTime),12,-15,5),
	(CAST(N'2022-02-26 02:06:43.000' AS DateTime),12,-8,17.6),

	(CAST(N'2022-02-26 02:02:43.000' AS DateTime),13,-14,6.8),
	(CAST(N'2022-02-26 02:02:53.000' AS DateTime),13,-10,14),
	(CAST(N'2022-02-26 02:03:03.000' AS DateTime),13,-5,23),
	(CAST(N'2022-02-26 02:03:13.000' AS DateTime),13,-13,8.6),
	(CAST(N'2022-02-26 02:03:23.000' AS DateTime),13,-7,19.4),
	(CAST(N'2022-02-26 02:03:33.000' AS DateTime),13,-5,23),
	(CAST(N'2022-02-26 02:03:43.000' AS DateTime),13,-11,12.2),
	(CAST(N'2022-02-26 02:03:53.000' AS DateTime),13,-6,21.2),
	(CAST(N'2022-02-26 02:04:03.000' AS DateTime),13,-13,8.6),
	(CAST(N'2022-02-26 02:04:13.000' AS DateTime),13,-8,17.6),
	(CAST(N'2022-02-26 02:04:23.000' AS DateTime),13,-5,23),
	(CAST(N'2022-02-26 02:04:33.000' AS DateTime),13,-13,8.6),
	(CAST(N'2022-02-26 02:04:43.000' AS DateTime),13,-10,14),
	(CAST(N'2022-02-26 02:04:53.000' AS DateTime),13,-11,12.2),
	(CAST(N'2022-02-26 02:05:03.000' AS DateTime),13,-10,14),
	(CAST(N'2022-02-26 02:05:13.000' AS DateTime),13,-8,17.6),
	(CAST(N'2022-02-26 02:05:23.000' AS DateTime),13,-8,17.6),
	(CAST(N'2022-02-26 02:05:33.000' AS DateTime),13,-10,14),
	(CAST(N'2022-02-26 02:05:43.000' AS DateTime),13,-8,17.6),
	(CAST(N'2022-02-26 02:05:53.000' AS DateTime),13,-12,10.4),
	(CAST(N'2022-02-26 02:06:03.000' AS DateTime),13,-13,8.6),
	(CAST(N'2022-02-26 02:06:13.000' AS DateTime),13,-10,14),
	(CAST(N'2022-02-26 02:06:23.000' AS DateTime),13,-11,12.2),
	(CAST(N'2022-02-26 02:06:33.000' AS DateTime),13,-6,21.2),
	(CAST(N'2022-02-26 02:06:43.000' AS DateTime),13,-8,17.6),

	(CAST(N'2022-02-26 02:02:43.000' AS DateTime),14,-8,17.6),
	(CAST(N'2022-02-26 02:02:53.000' AS DateTime),14,-13,8.6),
	(CAST(N'2022-02-26 02:03:03.000' AS DateTime),14,-11,12.2),
	(CAST(N'2022-02-26 02:03:13.000' AS DateTime),14,-6,21.2),
	(CAST(N'2022-02-26 02:03:23.000' AS DateTime),14,-14,6.8),
	(CAST(N'2022-02-26 02:03:33.000' AS DateTime),14,-9,15.8),
	(CAST(N'2022-02-26 02:03:43.000' AS DateTime),14,-7,19.4),
	(CAST(N'2022-02-26 02:03:53.000' AS DateTime),14,-10,14),
	(CAST(N'2022-02-26 02:04:03.000' AS DateTime),14,-11,12.2),
	(CAST(N'2022-02-26 02:04:13.000' AS DateTime),14,-6,21.2),
	(CAST(N'2022-02-26 02:04:23.000' AS DateTime),14,-10,14),
	(CAST(N'2022-02-26 02:04:33.000' AS DateTime),14,-5,23),
	(CAST(N'2022-02-26 02:04:43.000' AS DateTime),14,-9,15.8),
	(CAST(N'2022-02-26 02:04:53.000' AS DateTime),14,-7,19.4),
	(CAST(N'2022-02-26 02:05:03.000' AS DateTime),14,-8,17.6),
	(CAST(N'2022-02-26 02:05:13.000' AS DateTime),14,-13,8.6),
	(CAST(N'2022-02-26 02:05:23.000' AS DateTime),14,-13,8.6),
	(CAST(N'2022-02-26 02:05:33.000' AS DateTime),14,-13,8.6),
	(CAST(N'2022-02-26 02:05:43.000' AS DateTime),14,-7,19.4),
	(CAST(N'2022-02-26 02:05:53.000' AS DateTime),14,-14,6.8),
	(CAST(N'2022-02-26 02:06:03.000' AS DateTime),14,-9,15.8),
	(CAST(N'2022-02-26 02:06:13.000' AS DateTime),14,-5,23),
	(CAST(N'2022-02-26 02:06:23.000' AS DateTime),14,-8,17.6),
	(CAST(N'2022-02-26 02:06:33.000' AS DateTime),14,-5,23),
	(CAST(N'2022-02-26 02:06:43.000' AS DateTime),14,-6,21.2),

	(CAST(N'2022-02-26 02:02:43.000' AS DateTime),15,-15,5),
	(CAST(N'2022-02-26 02:02:53.000' AS DateTime),15,-13,8.6),
	(CAST(N'2022-02-26 02:03:03.000' AS DateTime),15,-8,17.6),
	(CAST(N'2022-02-26 02:03:13.000' AS DateTime),15,-13,8.6),
	(CAST(N'2022-02-26 02:03:23.000' AS DateTime),15,-9,15.8),
	(CAST(N'2022-02-26 02:03:33.000' AS DateTime),15,-10,14),
	(CAST(N'2022-02-26 02:03:43.000' AS DateTime),15,-15,5),
	(CAST(N'2022-02-26 02:03:53.000' AS DateTime),15,-9,15.8),
	(CAST(N'2022-02-26 02:04:03.000' AS DateTime),15,-7,19.4),
	(CAST(N'2022-02-26 02:04:13.000' AS DateTime),15,-7,19.4),
	(CAST(N'2022-02-26 02:04:23.000' AS DateTime),15,-6,21.2),
	(CAST(N'2022-02-26 02:04:33.000' AS DateTime),15,-6,21.2),
	(CAST(N'2022-02-26 02:04:43.000' AS DateTime),15,-9,15.8),
	(CAST(N'2022-02-26 02:04:53.000' AS DateTime),15,-6,21.2),
	(CAST(N'2022-02-26 02:05:03.000' AS DateTime),15,-7,19.4),
	(CAST(N'2022-02-26 02:05:13.000' AS DateTime),15,-10,14),
	(CAST(N'2022-02-26 02:05:23.000' AS DateTime),15,-10,14),
	(CAST(N'2022-02-26 02:05:33.000' AS DateTime),15,-8,17.6),
	(CAST(N'2022-02-26 02:05:43.000' AS DateTime),15,-15,5),
	(CAST(N'2022-02-26 02:05:53.000' AS DateTime),15,-13,8.6),
	(CAST(N'2022-02-26 02:06:03.000' AS DateTime),15,-7,19.4),
	(CAST(N'2022-02-26 02:06:13.000' AS DateTime),15,-8,17.6),
	(CAST(N'2022-02-26 02:06:23.000' AS DateTime),15,-14,6.8),
	(CAST(N'2022-02-26 02:06:33.000' AS DateTime),15,-6,21.2),
	(CAST(N'2022-02-26 02:06:43.000' AS DateTime),15,-11,12.2),

	(CAST(N'2022-02-26 02:02:43.000' AS DateTime),17,-12,10.4),
	(CAST(N'2022-02-26 02:02:53.000' AS DateTime),17,-7,19.4),
	(CAST(N'2022-02-26 02:03:03.000' AS DateTime),17,-9,15.8),
	(CAST(N'2022-02-26 02:03:13.000' AS DateTime),17,-5,23),
	(CAST(N'2022-02-26 02:03:23.000' AS DateTime),17,-9,15.8),
	(CAST(N'2022-02-26 02:03:33.000' AS DateTime),17,-6,21.2),
	(CAST(N'2022-02-26 02:03:43.000' AS DateTime),17,-7,19.4),
	(CAST(N'2022-02-26 02:03:53.000' AS DateTime),17,-9,15.8),
	(CAST(N'2022-02-26 02:04:03.000' AS DateTime),17,-7,19.4),
	(CAST(N'2022-02-26 02:04:13.000' AS DateTime),17,-7,19.4),
	(CAST(N'2022-02-26 02:04:23.000' AS DateTime),17,-6,21.2),
	(CAST(N'2022-02-26 02:04:33.000' AS DateTime),17,-14,6.8),
	(CAST(N'2022-02-26 02:04:43.000' AS DateTime),17,-15,5),
	(CAST(N'2022-02-26 02:04:53.000' AS DateTime),17,-8,17.6),
	(CAST(N'2022-02-26 02:05:03.000' AS DateTime),17,-12,10.4),
	(CAST(N'2022-02-26 02:05:13.000' AS DateTime),17,-6,21.2),
	(CAST(N'2022-02-26 02:05:23.000' AS DateTime),17,-6,21.2),
	(CAST(N'2022-02-26 02:05:33.000' AS DateTime),17,-13,8.6),
	(CAST(N'2022-02-26 02:05:43.000' AS DateTime),17,-6,21.2),
	(CAST(N'2022-02-26 02:05:53.000' AS DateTime),17,-14,6.8),
	(CAST(N'2022-02-26 02:06:03.000' AS DateTime),17,-7,19.4),
	(CAST(N'2022-02-26 02:06:13.000' AS DateTime),17,-14,6.8),
	(CAST(N'2022-02-26 02:06:23.000' AS DateTime),17,-7,19.4),
	(CAST(N'2022-02-26 02:06:33.000' AS DateTime),17,-7,19.4),
	(CAST(N'2022-02-26 02:06:43.000' AS DateTime),17,-7,19.4),

	(CAST(N'2022-02-26 02:02:43.000' AS DateTime),18,-11,12.2),
	(CAST(N'2022-02-26 02:02:53.000' AS DateTime),18,-14,6.8),
	(CAST(N'2022-02-26 02:03:03.000' AS DateTime),18,-9,15.8),
	(CAST(N'2022-02-26 02:03:13.000' AS DateTime),18,-6,21.2),
	(CAST(N'2022-02-26 02:03:23.000' AS DateTime),18,-13,8.6),
	(CAST(N'2022-02-26 02:03:33.000' AS DateTime),18,-8,17.6),
	(CAST(N'2022-02-26 02:03:43.000' AS DateTime),18,-15,5),
	(CAST(N'2022-02-26 02:03:53.000' AS DateTime),18,-7,19.4),
	(CAST(N'2022-02-26 02:04:03.000' AS DateTime),18,-13,8.6),
	(CAST(N'2022-02-26 02:04:13.000' AS DateTime),18,-15,5),
	(CAST(N'2022-02-26 02:04:23.000' AS DateTime),18,-14,6.8),
	(CAST(N'2022-02-26 02:04:33.000' AS DateTime),18,-7,19.4),
	(CAST(N'2022-02-26 02:04:43.000' AS DateTime),18,-15,5),
	(CAST(N'2022-02-26 02:04:53.000' AS DateTime),18,-5,23),
	(CAST(N'2022-02-26 02:05:03.000' AS DateTime),18,-8,17.6),
	(CAST(N'2022-02-26 02:05:13.000' AS DateTime),18,-14,6.8),
	(CAST(N'2022-02-26 02:05:23.000' AS DateTime),18,-9,15.8),
	(CAST(N'2022-02-26 02:05:33.000' AS DateTime),18,-9,15.8),
	(CAST(N'2022-02-26 02:05:43.000' AS DateTime),18,-10,14),
	(CAST(N'2022-02-26 02:05:53.000' AS DateTime),18,-8,17.6),
	(CAST(N'2022-02-26 02:06:03.000' AS DateTime),18,-14,6.8),
	(CAST(N'2022-02-26 02:06:13.000' AS DateTime),18,-10,14),
	(CAST(N'2022-02-26 02:06:23.000' AS DateTime),18,-10,14),
	(CAST(N'2022-02-26 02:06:33.000' AS DateTime),18,-9,15.8),
	(CAST(N'2022-02-26 02:06:43.000' AS DateTime),18,-8,17.6),

	(CAST(N'2022-02-26 02:02:43.000' AS DateTime),19,-13,8.6),
	(CAST(N'2022-02-26 02:02:53.000' AS DateTime),19,-10,14),
	(CAST(N'2022-02-26 02:03:03.000' AS DateTime),19,-8,17.6),
	(CAST(N'2022-02-26 02:03:13.000' AS DateTime),19,-14,6.8),
	(CAST(N'2022-02-26 02:03:23.000' AS DateTime),19,-13,8.6),
	(CAST(N'2022-02-26 02:03:33.000' AS DateTime),19,-6,21.2),
	(CAST(N'2022-02-26 02:03:43.000' AS DateTime),19,-11,12.2),
	(CAST(N'2022-02-26 02:03:53.000' AS DateTime),19,-5,23),
	(CAST(N'2022-02-26 02:04:03.000' AS DateTime),19,-14,6.8),
	(CAST(N'2022-02-26 02:04:13.000' AS DateTime),19,-11,12.2),
	(CAST(N'2022-02-26 02:04:23.000' AS DateTime),19,-12,10.4),
	(CAST(N'2022-02-26 02:04:33.000' AS DateTime),19,-5,23),
	(CAST(N'2022-02-26 02:04:43.000' AS DateTime),19,-12,10.4),
	(CAST(N'2022-02-26 02:04:53.000' AS DateTime),19,-13,8.6),
	(CAST(N'2022-02-26 02:05:03.000' AS DateTime),19,-6,21.2),
	(CAST(N'2022-02-26 02:05:13.000' AS DateTime),19,-13,8.6),
	(CAST(N'2022-02-26 02:05:23.000' AS DateTime),19,-10,14),
	(CAST(N'2022-02-26 02:05:33.000' AS DateTime),19,-9,15.8),
	(CAST(N'2022-02-26 02:05:43.000' AS DateTime),19,-15,5),
	(CAST(N'2022-02-26 02:05:53.000' AS DateTime),19,-13,8.6),
	(CAST(N'2022-02-26 02:06:03.000' AS DateTime),19,-9,15.8),
	(CAST(N'2022-02-26 02:06:13.000' AS DateTime),19,-10,14),
	(CAST(N'2022-02-26 02:06:23.000' AS DateTime),19,-6,21.2),
	(CAST(N'2022-02-26 02:06:33.000' AS DateTime),19,-15,5),
	(CAST(N'2022-02-26 02:06:43.000' AS DateTime),19,-7,19.4),

	(CAST(N'2022-02-26 02:02:43.000' AS DateTime),20,-8,17.6),
	(CAST(N'2022-02-26 02:02:53.000' AS DateTime),20,-12,10.4),
	(CAST(N'2022-02-26 02:03:03.000' AS DateTime),20,-15,5),
	(CAST(N'2022-02-26 02:03:13.000' AS DateTime),20,-5,23),
	(CAST(N'2022-02-26 02:03:23.000' AS DateTime),20,-7,19.4),
	(CAST(N'2022-02-26 02:03:33.000' AS DateTime),20,-9,15.8),
	(CAST(N'2022-02-26 02:03:43.000' AS DateTime),20,-9,15.8),
	(CAST(N'2022-02-26 02:03:53.000' AS DateTime),20,-13,8.6),
	(CAST(N'2022-02-26 02:04:03.000' AS DateTime),20,-14,6.8),
	(CAST(N'2022-02-26 02:04:13.000' AS DateTime),20,-13,8.6),
	(CAST(N'2022-02-26 02:04:23.000' AS DateTime),20,-15,5),
	(CAST(N'2022-02-26 02:04:33.000' AS DateTime),20,-10,14),
	(CAST(N'2022-02-26 02:04:43.000' AS DateTime),20,-14,6.8),
	(CAST(N'2022-02-26 02:04:53.000' AS DateTime),20,-8,17.6),
	(CAST(N'2022-02-26 02:05:03.000' AS DateTime),20,-5,23),
	(CAST(N'2022-02-26 02:05:13.000' AS DateTime),20,-7,19.4),
	(CAST(N'2022-02-26 02:05:23.000' AS DateTime),20,-11,12.2),
	(CAST(N'2022-02-26 02:05:33.000' AS DateTime),20,-12,10.4),
	(CAST(N'2022-02-26 02:05:43.000' AS DateTime),20,-15,5),
	(CAST(N'2022-02-26 02:05:53.000' AS DateTime),20,-12,10.4),
	(CAST(N'2022-02-26 02:06:03.000' AS DateTime),20,-12,10.4),
	(CAST(N'2022-02-26 02:06:13.000' AS DateTime),20,-5,23),
	(CAST(N'2022-02-26 02:06:23.000' AS DateTime),20,-5,23),
	(CAST(N'2022-02-26 02:06:33.000' AS DateTime),20,-10,14),
	(CAST(N'2022-02-26 02:06:43.000' AS DateTime),20,-8,17.6),

	(CAST(N'2022-02-26 02:02:43.000' AS DateTime),21,-10,14),
	(CAST(N'2022-02-26 02:02:53.000' AS DateTime),21,-12,10.4),
	(CAST(N'2022-02-26 02:03:03.000' AS DateTime),21,-11,12.2),
	(CAST(N'2022-02-26 02:03:13.000' AS DateTime),21,-12,10.4),
	(CAST(N'2022-02-26 02:03:23.000' AS DateTime),21,-9,15.8),
	(CAST(N'2022-02-26 02:03:33.000' AS DateTime),21,-7,19.4),
	(CAST(N'2022-02-26 02:03:43.000' AS DateTime),21,-9,15.8),
	(CAST(N'2022-02-26 02:03:53.000' AS DateTime),21,-15,5),
	(CAST(N'2022-02-26 02:04:03.000' AS DateTime),21,-13,8.6),
	(CAST(N'2022-02-26 02:04:13.000' AS DateTime),21,-12,10.4),
	(CAST(N'2022-02-26 02:04:23.000' AS DateTime),21,-7,19.4),
	(CAST(N'2022-02-26 02:04:33.000' AS DateTime),21,-6,21.2),
	(CAST(N'2022-02-26 02:04:43.000' AS DateTime),21,-11,12.2),
	(CAST(N'2022-02-26 02:04:53.000' AS DateTime),21,-9,15.8),
	(CAST(N'2022-02-26 02:05:03.000' AS DateTime),21,-5,23),
	(CAST(N'2022-02-26 02:05:13.000' AS DateTime),21,-15,5),
	(CAST(N'2022-02-26 02:05:23.000' AS DateTime),21,-7,19.4),
	(CAST(N'2022-02-26 02:05:33.000' AS DateTime),21,-14,6.8),
	(CAST(N'2022-02-26 02:05:43.000' AS DateTime),21,-7,19.4),
	(CAST(N'2022-02-26 02:05:53.000' AS DateTime),21,-10,14),
	(CAST(N'2022-02-26 02:06:03.000' AS DateTime),21,-12,10.4),
	(CAST(N'2022-02-26 02:06:13.000' AS DateTime),21,-8,17.6),
	(CAST(N'2022-02-26 02:06:23.000' AS DateTime),21,-15,5),
	(CAST(N'2022-02-26 02:06:33.000' AS DateTime),21,-8,17.6),
	(CAST(N'2022-02-26 02:06:43.000' AS DateTime),21,-8,17.6),

	(CAST(N'2022-02-26 02:02:43.000' AS DateTime),22,-13,8.6),
	(CAST(N'2022-02-26 02:02:53.000' AS DateTime),22,-6,21.2),
	(CAST(N'2022-02-26 02:03:03.000' AS DateTime),22,-15,5),
	(CAST(N'2022-02-26 02:03:13.000' AS DateTime),22,-9,15.8),
	(CAST(N'2022-02-26 02:03:23.000' AS DateTime),22,-11,12.2),
	(CAST(N'2022-02-26 02:03:33.000' AS DateTime),22,-14,6.8),
	(CAST(N'2022-02-26 02:03:43.000' AS DateTime),22,-8,17.6),
	(CAST(N'2022-02-26 02:03:53.000' AS DateTime),22,-5,23),
	(CAST(N'2022-02-26 02:04:03.000' AS DateTime),22,-5,23),
	(CAST(N'2022-02-26 02:04:13.000' AS DateTime),22,-15,5),
	(CAST(N'2022-02-26 02:04:23.000' AS DateTime),22,-7,19.4),
	(CAST(N'2022-02-26 02:04:33.000' AS DateTime),22,-11,12.2),
	(CAST(N'2022-02-26 02:04:43.000' AS DateTime),22,-9,15.8),
	(CAST(N'2022-02-26 02:04:53.000' AS DateTime),22,-9,15.8),
	(CAST(N'2022-02-26 02:05:03.000' AS DateTime),22,-12,10.4),
	(CAST(N'2022-02-26 02:05:13.000' AS DateTime),22,-5,23),
	(CAST(N'2022-02-26 02:05:23.000' AS DateTime),22,-9,15.8),
	(CAST(N'2022-02-26 02:05:33.000' AS DateTime),22,-12,10.4),
	(CAST(N'2022-02-26 02:05:43.000' AS DateTime),22,-10,14),
	(CAST(N'2022-02-26 02:05:53.000' AS DateTime),22,-14,6.8),
	(CAST(N'2022-02-26 02:06:03.000' AS DateTime),22,-13,8.6),
	(CAST(N'2022-02-26 02:06:13.000' AS DateTime),22,-5,23),
	(CAST(N'2022-02-26 02:06:23.000' AS DateTime),22,-13,8.6),
	(CAST(N'2022-02-26 02:06:33.000' AS DateTime),22,-9,15.8),
	(CAST(N'2022-02-26 02:06:43.000' AS DateTime),22,-9,15.8),

	(CAST(N'2022-02-26 02:02:43.000' AS DateTime),23,-7,19.4),
	(CAST(N'2022-02-26 02:02:53.000' AS DateTime),23,-11,12.2),
	(CAST(N'2022-02-26 02:03:03.000' AS DateTime),23,-5,23),
	(CAST(N'2022-02-26 02:03:13.000' AS DateTime),23,-8,17.6),
	(CAST(N'2022-02-26 02:03:23.000' AS DateTime),23,-5,23),
	(CAST(N'2022-02-26 02:03:33.000' AS DateTime),23,-5,23),
	(CAST(N'2022-02-26 02:03:43.000' AS DateTime),23,-6,21.2),
	(CAST(N'2022-02-26 02:03:53.000' AS DateTime),23,-10,14),
	(CAST(N'2022-02-26 02:04:03.000' AS DateTime),23,-10,14),
	(CAST(N'2022-02-26 02:04:13.000' AS DateTime),23,-15,5),
	(CAST(N'2022-02-26 02:04:23.000' AS DateTime),23,-13,8.6),
	(CAST(N'2022-02-26 02:04:33.000' AS DateTime),23,-13,8.6),
	(CAST(N'2022-02-26 02:04:43.000' AS DateTime),23,-15,5),
	(CAST(N'2022-02-26 02:04:53.000' AS DateTime),23,-8,17.6),
	(CAST(N'2022-02-26 02:05:03.000' AS DateTime),23,-13,8.6),
	(CAST(N'2022-02-26 02:05:13.000' AS DateTime),23,-5,23),
	(CAST(N'2022-02-26 02:05:23.000' AS DateTime),23,-13,8.6),
	(CAST(N'2022-02-26 02:05:33.000' AS DateTime),23,-12,10.4),
	(CAST(N'2022-02-26 02:05:43.000' AS DateTime),23,-13,8.6),
	(CAST(N'2022-02-26 02:05:53.000' AS DateTime),23,-13,8.6),
	(CAST(N'2022-02-26 02:06:03.000' AS DateTime),23,-8,17.6),
	(CAST(N'2022-02-26 02:06:13.000' AS DateTime),23,-7,19.4),
	(CAST(N'2022-02-26 02:06:23.000' AS DateTime),23,-13,8.6),
	(CAST(N'2022-02-26 02:06:33.000' AS DateTime),23,-6,21.2),
	(CAST(N'2022-02-26 02:06:43.000' AS DateTime),23,-15,5),

	(CAST(N'2022-02-26 02:02:43.000' AS DateTime),24,-7,19.4),
	(CAST(N'2022-02-26 02:02:53.000' AS DateTime),24,-12,10.4),
	(CAST(N'2022-02-26 02:03:03.000' AS DateTime),24,-13,8.6),
	(CAST(N'2022-02-26 02:03:13.000' AS DateTime),24,-13,8.6),
	(CAST(N'2022-02-26 02:03:23.000' AS DateTime),24,-15,5),
	(CAST(N'2022-02-26 02:03:33.000' AS DateTime),24,-12,10.4),
	(CAST(N'2022-02-26 02:03:43.000' AS DateTime),24,-15,5),
	(CAST(N'2022-02-26 02:03:53.000' AS DateTime),24,-10,14),
	(CAST(N'2022-02-26 02:04:03.000' AS DateTime),24,-7,19.4),
	(CAST(N'2022-02-26 02:04:13.000' AS DateTime),24,-11,12.2),
	(CAST(N'2022-02-26 02:04:23.000' AS DateTime),24,-9,15.8),
	(CAST(N'2022-02-26 02:04:33.000' AS DateTime),24,-9,15.8),
	(CAST(N'2022-02-26 02:04:43.000' AS DateTime),24,-14,6.8),
	(CAST(N'2022-02-26 02:04:53.000' AS DateTime),24,-7,19.4),
	(CAST(N'2022-02-26 02:05:03.000' AS DateTime),24,-6,21.2),
	(CAST(N'2022-02-26 02:05:13.000' AS DateTime),24,-5,23),
	(CAST(N'2022-02-26 02:05:23.000' AS DateTime),24,-13,8.6),
	(CAST(N'2022-02-26 02:05:33.000' AS DateTime),24,-10,14),
	(CAST(N'2022-02-26 02:05:43.000' AS DateTime),24,-7,19.4),
	(CAST(N'2022-02-26 02:05:53.000' AS DateTime),24,-15,5),
	(CAST(N'2022-02-26 02:06:03.000' AS DateTime),24,-10,14),
	(CAST(N'2022-02-26 02:06:13.000' AS DateTime),24,-15,5),
	(CAST(N'2022-02-26 02:06:23.000' AS DateTime),24,-15,5),
	(CAST(N'2022-02-26 02:06:33.000' AS DateTime),24,-13,8.6),
	(CAST(N'2022-02-26 02:06:43.000' AS DateTime),24,-8,17.6)

GO