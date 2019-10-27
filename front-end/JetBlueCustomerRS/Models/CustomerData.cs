using System.Data.Entity.ModelConfiguration;
using System.ComponentModel.DataAnnotations.Schema;

[System.ComponentModel.DataAnnotations.Schema.Table("reviews")]
public class CustomerData
{
    [System.ComponentModel.DataAnnotations.Key]
    public System.String review_title { get; set; }
    public System.String review_details { get; set; }
    public System.String source { get; set; }
    public System.String author { get; set; }
    public int likes { get; set; }
    public System.DateTime date_created { get; set; }
    public System.String url { get; set; }
    public System.String location { get; set; }
    public float sentiment { get; set; }
    public float sentiment_magnitude { get; set; }
    public System.String adjectives { get; set; }
    public System.String adverbs { get; set; }
    public float entity_1_salience { get; set; }
    public float entity_1_sentiment { get; set; }
    public float entity_2_salience { get; set; }
    public float entity_2_sentiment { get; set; }
    public float entity_3_salience { get; set; }
    public float entity_3_sentiment { get; set; }
    public float entity_4_salience { get; set; }
    public float entity_4_sentiment { get; set; }

}