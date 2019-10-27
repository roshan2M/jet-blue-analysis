using System.Data.Entity;
using System.Data.Entity.Infrastructure;
using System.Data.Entity.ModelConfiguration.Conventions;

class GoogleBigQueryContext : DbContext
{
    public GoogleBigQueryContext() { }

    public DbSet<CustomerData> customerDatas { set; get; }

    protected override void OnModelCreating(DbModelBuilder modelBuilder)
    {
        // To remove the requests to the Migration History table
        Database.SetInitializer<GoogleBigQueryContext>(null);
        // To remove the plural names   
        modelBuilder.Conventions.Remove<PluralizingTableNameConvention>();
    }
}