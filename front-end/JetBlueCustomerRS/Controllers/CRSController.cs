using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using JetBlueCRS;
using System.Web.Mvc;
using Google.Cloud.BigQuery.V2;
using Google.Apis.Auth.OAuth2;

namespace JetBlueCRS.Controllers
{
    public class CRSController : Controller
    {
        // GET: CRS
        public ActionResult Index()
        {
            return View();
        }

        // GET: CRS
        public ActionResult Cost()
        {
            //string projectId = "smart-inn-257104";
            //var client = BigQueryClient.Create(projectId);
            //string query = @"SELECT
            //    CONCAT(
            //        'https://stackoverflow.com/questions/',
            //        CAST(id as STRING)) as url, view_count
            //    FROM `bigquery-public-data.stackoverflow.posts_questions`
            //    WHERE tags like '%google-bigquery%'
            //    ORDER BY view_count DESC
            //    LIMIT 10";
            //var result = client.ExecuteQuery(query, parameters: null);
            //Console.Write("\nQuery Results:\n------------\n");
            //foreach (var row in result)
            //{
            //    Console.WriteLine($"{row["url"]}: {row["view_count"]} views");
            //}
            GoogleBigQueryContext context = new GoogleBigQueryContext();
            
            //List<CustomerData> datas = context.customerDatas.ToList();
            List<DataPoint> dataPoints = new List<DataPoint>();

            dataPoints.Add(new DataPoint("USA", 121));
            dataPoints.Add(new DataPoint("Great Britain", 67));
            dataPoints.Add(new DataPoint("China", 70));
            dataPoints.Add(new DataPoint("Russia", 56));
            dataPoints.Add(new DataPoint("Germany", -42));
            dataPoints.Add(new DataPoint("Japan", 41));
            dataPoints.Add(new DataPoint("France", 42));
            dataPoints.Add(new DataPoint("South Korea", 21));

            ViewBag.DataPoints = Newtonsoft.Json.JsonConvert.SerializeObject(dataPoints);
            return View();
        }

        // GET: CRS
        public ActionResult Food()
        {
            List<DataPoint> dataPoints = new List<DataPoint>();

            dataPoints.Add(new DataPoint("Chicken", 1.7));
            dataPoints.Add(new DataPoint("Fish", -0.9));
            dataPoints.Add(new DataPoint("Beef", 1));
            dataPoints.Add(new DataPoint("Salad", 0.75));
            dataPoints.Add(new DataPoint("Wine and Alcohol", -0.3));
            dataPoints.Add(new DataPoint("Snack (Treats)", 2));
            dataPoints.Add(new DataPoint("Snack (Chips)", -0.1));

            ViewBag.DataPoints = Newtonsoft.Json.JsonConvert.SerializeObject(dataPoints);
            return View();
        }

        // GET: CRS
        public ActionResult Entertainment()
        {
            List<DataPoint> dataPoints = new List<DataPoint>();

            dataPoints.Add(new DataPoint("-inf to -2", 8));
            dataPoints.Add(new DataPoint("-2 to -1", 17));
            dataPoints.Add(new DataPoint("-1 to 0", 67));
            dataPoints.Add(new DataPoint("0 to 1", 70));
            dataPoints.Add(new DataPoint("1 to 2", 94));
            dataPoints.Add(new DataPoint("2 to inf", 6));

            ViewBag.DataPoints = Newtonsoft.Json.JsonConvert.SerializeObject(dataPoints);
            return View();
        }

        // GET: CRS
        public ActionResult Service()
        {
            List<DataPoint> dataPoints = new List<DataPoint>();

            dataPoints.Add(new DataPoint("Service (General)", 25));
            dataPoints.Add(new DataPoint("Customer Service", 10));
            dataPoints.Add(new DataPoint("Management", 40));
            dataPoints.Add(new DataPoint("Business", 20));
            dataPoints.Add(new DataPoint("Bookings", 6));
            dataPoints.Add(new DataPoint("Seatings", 10));

            ViewBag.DataPoints = Newtonsoft.Json.JsonConvert.SerializeObject(dataPoints);
            return View();
        }
  
    }
}