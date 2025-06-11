USE [master]
GO
/****** Object:  Database [AIRBNB_star_dwh]    Script Date: 11.06.2025 15:36:18 ******/
CREATE DATABASE [AIRBNB_star_dwh]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'AIRBNB_star_wh', FILENAME = N'D:\STUDIA\Semestr 6\Hurtownie danych i systemy Business Intelligence\Laboratoria\Projekt\db\AIRBNB_star_wh.mdf' , SIZE = 7610368KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'AIRBNB_star_wh_log', FILENAME = N'D:\STUDIA\Semestr 6\Hurtownie danych i systemy Business Intelligence\Laboratoria\Projekt\db\AIRBNB_star_wh_log.ldf' , SIZE = 33431552KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [AIRBNB_star_dwh] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [AIRBNB_star_dwh].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [AIRBNB_star_dwh] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET ARITHABORT OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET  DISABLE_BROKER 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET RECOVERY FULL 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET  MULTI_USER 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [AIRBNB_star_dwh] SET DB_CHAINING OFF 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [AIRBNB_star_dwh] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
EXEC sys.sp_db_vardecimal_storage_format N'AIRBNB_star_dwh', N'ON'
GO
ALTER DATABASE [AIRBNB_star_dwh] SET QUERY_STORE = OFF
GO
USE [AIRBNB_star_dwh]
GO
/****** Object:  User [LAPTOP-826FGFSL\flang]    Script Date: 11.06.2025 15:36:18 ******/
CREATE USER [LAPTOP-826FGFSL\flang] FOR LOGIN [LAPTOP-826FGFSL\flang] WITH DEFAULT_SCHEMA=[dbo]
GO
ALTER ROLE [db_owner] ADD MEMBER [LAPTOP-826FGFSL\flang]
GO
ALTER ROLE [db_datareader] ADD MEMBER [LAPTOP-826FGFSL\flang]
GO
ALTER ROLE [db_datawriter] ADD MEMBER [LAPTOP-826FGFSL\flang]
GO
/****** Object:  Table [dbo].[Dim_Date]    Script Date: 11.06.2025 15:36:19 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Dim_Date](
	[date] [date] NOT NULL,
	[Day] [tinyint] NULL,
	[DaySuffix] [char](2) NULL,
	[Weekday] [tinyint] NULL,
	[WeekDayName] [varchar](10) NULL,
	[IsWeekend] [bit] NULL,
	[IsHoliday] [bit] NULL,
	[DOWInMonth] [tinyint] NULL,
	[DayOfYear] [smallint] NULL,
	[WeekOfMonth] [tinyint] NULL,
	[WeekOfYear] [tinyint] NULL,
	[ISOWeekOfYear] [tinyint] NULL,
	[Month] [tinyint] NULL,
	[MonthName] [varchar](10) NULL,
	[Quarter] [tinyint] NULL,
	[QuarterName] [varchar](6) NULL,
	[Year] [int] NULL,
	[MMYYYY] [char](6) NULL,
	[MonthYear] [char](7) NULL,
	[FirstDayOfMonth] [date] NULL,
	[LastDayOfMonth] [date] NULL,
	[FirstDayOfQuarter] [date] NULL,
	[LastDayOfQuarter] [date] NULL,
	[FirstDayOfYear] [date] NULL,
	[LastDayOfYear] [date] NULL,
	[HolidayText] [nvarchar](100) NULL,
 CONSTRAINT [PK_Dim_Date] PRIMARY KEY CLUSTERED 
(
	[date] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Dim_Property]    Script Date: 11.06.2025 15:36:19 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Dim_Property](
	[property_id] [bigint] NOT NULL,
	[last_scraped] [date] NULL,
	[property_name] [nvarchar](255) NULL,
	[host_id] [bigint] NULL,
	[host_name] [nvarchar](100) NULL,
	[host_since] [date] NULL,
	[host_response_time] [nvarchar](50) NULL,
	[host_response_rate] [float] NULL,
	[host_acceptance_rate] [float] NULL,
	[host_is_superhost] [nvarchar](3) NULL,
	[host_listings_count] [int] NULL,
	[host_total_listings_count] [int] NULL,
	[host_identity_verified] [nvarchar](3) NULL,
	[latitude] [float] NULL,
	[longitude] [float] NULL,
	[property_type] [nvarchar](100) NULL,
	[room_type] [nvarchar](100) NULL,
	[accommodates] [int] NULL,
	[bathrooms] [float] NULL,
	[bedrooms] [int] NULL,
	[beds] [int] NULL,
	[price] [float] NULL,
	[minimum_nights] [int] NULL,
	[maximum_nights] [int] NULL,
	[has_availability] [nvarchar](3) NULL,
	[availability_30] [int] NULL,
	[availability_60] [int] NULL,
	[availability_90] [int] NULL,
	[availability_365] [int] NULL,
	[number_of_reviews] [int] NULL,
	[number_of_reviews_ltm] [int] NULL,
	[number_of_reviews_l30d] [int] NULL,
	[review_scores_rating] [float] NULL,
	[review_scores_accuracy] [float] NULL,
	[review_scores_cleanliness] [float] NULL,
	[review_scores_checkin] [float] NULL,
	[review_scores_communication] [float] NULL,
	[review_scores_location] [float] NULL,
	[review_scores_value] [float] NULL,
	[instant_bookable] [nvarchar](3) NULL,
	[calculated_host_listings_count] [int] NULL,
	[calculated_host_listings_count_entire_homes] [int] NULL,
	[calculated_host_listings_count_private_rooms] [int] NULL,
	[calculated_host_listings_count_shared_rooms] [int] NULL,
	[reviews_per_month] [float] NULL,
	[scrape_date] [int] NULL,
	[country] [nvarchar](100) NULL,
	[region] [nvarchar](100) NULL,
	[city] [nvarchar](100) NULL,
	[isActive] [nvarchar](3) NULL,
	[vaildFrom] [bigint] NULL,
	[validTo] [bigint] NULL,
	[property_sk] [bigint] IDENTITY(1,1) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[property_sk] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Dim_Weather]    Script Date: 11.06.2025 15:36:19 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Dim_Weather](
	[weather_id] [nvarchar](50) NOT NULL,
	[date] [date] NULL,
	[location_name] [nvarchar](100) NULL,
	[avg_temp] [float] NULL,
	[max_temp] [float] NULL,
	[min_temp] [float] NULL,
	[daily_will_it_rain] [nvarchar](3) NULL,
	[daily_will_it_snow] [nvarchar](3) NULL,
	[daily_chance_of_rain] [float] NULL,
	[daily_chance_of_snow] [float] NULL,
	[sunrise] [time](7) NULL,
	[sunset] [time](7) NULL,
	[last_modified_date] [date] NULL,
 CONSTRAINT [PK_Dim_Weather] PRIMARY KEY CLUSTERED 
(
	[weather_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Fact_Offers]    Script Date: 11.06.2025 15:36:19 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Fact_Offers](
	[offer_id] [bigint] IDENTITY(1,1) NOT NULL,
	[property_id] [bigint] NULL,
	[offer_date] [date] NULL,
	[available] [nvarchar](3) NULL,
	[price] [money] NULL,
	[minimum_nights] [float] NULL,
	[maximum_nights] [float] NULL,
	[weather_id] [nvarchar](50) NULL,
	[scrape_date] [int] NULL,
	[country] [nvarchar](100) NULL,
	[region] [nvarchar](100) NULL,
	[city] [nvarchar](100) NULL,
 CONSTRAINT [PK_TwojaTabela_offer_id] PRIMARY KEY CLUSTERED 
(
	[offer_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Fact_Review]    Script Date: 11.06.2025 15:36:19 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Fact_Review](
	[review_id] [bigint] IDENTITY(1,1) NOT NULL,
	[property_id] [bigint] NULL,
	[date] [date] NULL,
	[reviewer_name] [nvarchar](100) NULL,
	[reviewer_id] [bigint] NULL,
	[scrape_date] [int] NULL,
	[country] [nvarchar](100) NULL,
	[region] [nvarchar](100) NULL,
	[city] [nvarchar](100) NULL,
 CONSTRAINT [PK_Fact_Review_review_id] PRIMARY KEY CLUSTERED 
(
	[review_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Fact_Offers]  WITH CHECK ADD  CONSTRAINT [FK_Fact_Offers_Dim_Date] FOREIGN KEY([offer_date])
REFERENCES [dbo].[Dim_Date] ([date])
GO
ALTER TABLE [dbo].[Fact_Offers] CHECK CONSTRAINT [FK_Fact_Offers_Dim_Date]
GO
ALTER TABLE [dbo].[Fact_Offers]  WITH CHECK ADD  CONSTRAINT [FK_Fact_Offers_Dim_Property] FOREIGN KEY([property_id])
REFERENCES [dbo].[Dim_Property] ([property_sk])
GO
ALTER TABLE [dbo].[Fact_Offers] CHECK CONSTRAINT [FK_Fact_Offers_Dim_Property]
GO
ALTER TABLE [dbo].[Fact_Offers]  WITH CHECK ADD  CONSTRAINT [FK_Fact_Offers_Dim_Weather] FOREIGN KEY([weather_id])
REFERENCES [dbo].[Dim_Weather] ([weather_id])
GO
ALTER TABLE [dbo].[Fact_Offers] CHECK CONSTRAINT [FK_Fact_Offers_Dim_Weather]
GO
ALTER TABLE [dbo].[Fact_Review]  WITH CHECK ADD  CONSTRAINT [FK_Fact_Review_Dim_Date1] FOREIGN KEY([date])
REFERENCES [dbo].[Dim_Date] ([date])
GO
ALTER TABLE [dbo].[Fact_Review] CHECK CONSTRAINT [FK_Fact_Review_Dim_Date1]
GO
ALTER TABLE [dbo].[Fact_Review]  WITH CHECK ADD  CONSTRAINT [FK_Fact_Review_Dim_Property] FOREIGN KEY([property_id])
REFERENCES [dbo].[Dim_Property] ([property_sk])
GO
ALTER TABLE [dbo].[Fact_Review] CHECK CONSTRAINT [FK_Fact_Review_Dim_Property]
GO
USE [master]
GO
ALTER DATABASE [AIRBNB_star_dwh] SET  READ_WRITE 
GO
