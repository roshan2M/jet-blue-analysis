using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using JetBlueCRS;
using System.Web.Mvc;

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
        public ActionResult Entertainment()
        {
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
        public ActionResult Service()
        {
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
  
    }
}