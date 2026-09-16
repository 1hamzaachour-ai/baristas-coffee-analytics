// =============================================================================
// BARISTAS COFFEE SHOP — POWER QUERY IMPORT SCRIPTS
// =============================================================================
// How to use each block:
//   1. Power BI Desktop -> Home -> Get Data -> Blank Query
//   2. Home -> Advanced Editor
//   3. Delete the placeholder text, paste ONE block below, click Done
//   4. Home -> Close & Apply (after pasting all 7)
// The query name Power BI gives a blank query is "Query1" etc. — rename it
// in the Queries pane (right-click -> Rename) to the name in each header
// comment below (Fact_Sales, Dim_Date, ...) so it matches the DAX file.
//
// Paths are hardcoded to this machine. If you move the project, edit the
// path string in each block (Ctrl+H in Advanced Editor, or just retype it).
// =============================================================================

// ----- Query name: Fact_Sales -----------------------------------------------
let
    Source = Csv.Document(File.Contents("C:\Users\MSI\Desktop\New folder\baristas-coffee-analytics\data_generator\data\fact_sales.csv"),[Delimiter=",", Columns=14, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers,{
        {"SalesLineID", Int64.Type}, {"TransactionID", Int64.Type}, {"DateKey", Int64.Type},
        {"TimeKey", Int64.Type}, {"StoreKey", Int64.Type}, {"ProductKey", Int64.Type},
        {"PaymentKey", Int64.Type}, {"ChannelKey", Int64.Type}, {"Quantity", Int64.Type},
        {"UnitPriceTND", type number}, {"UnitCostTND", type number},
        {"LineRevenueTND", type number}, {"LineCostTND", type number}, {"LineProfitTND", type number}
    })
in
    Typed

// ----- Query name: Dim_Date --------------------------------------------------
let
    Source = Csv.Document(File.Contents("C:\Users\MSI\Desktop\New folder\baristas-coffee-analytics\data_generator\data\dim_date.csv"),[Delimiter=",", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers,{
        {"DateKey", Int64.Type}, {"Date", type date}, {"Day", Int64.Type},
        {"DayName", type text}, {"DayOfWeekNum", Int64.Type}, {"IsWeekend", type logical},
        {"Month", Int64.Type}, {"MonthName", type text}, {"MonthYear", type text},
        {"Quarter", type text}, {"Year", Int64.Type}
    })
in
    Typed

// ----- Query name: Dim_Time --------------------------------------------------
let
    Source = Csv.Document(File.Contents("C:\Users\MSI\Desktop\New folder\baristas-coffee-analytics\data_generator\data\dim_time.csv"),[Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers,{
        {"TimeKey", Int64.Type}, {"Hour", Int64.Type}, {"Minute", Int64.Type}, {"TimeSlot", type text}
    })
in
    Typed

// ----- Query name: Dim_Store -------------------------------------------------
let
    Source = Csv.Document(File.Contents("C:\Users\MSI\Desktop\New folder\baristas-coffee-analytics\data_generator\data\dim_store.csv"),[Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers,{
        {"StoreKey", Int64.Type}, {"StoreName", type text}, {"City", type text},
        {"Region", type text}, {"StoreType", type text}, {"OpenDate", type date}
    })
in
    Typed

// ----- Query name: Dim_Product ------------------------------------------------
let
    Source = Csv.Document(File.Contents("C:\Users\MSI\Desktop\New folder\baristas-coffee-analytics\data_generator\data\dim_products.csv"),[Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers,{
        {"ProductKey", Int64.Type}, {"ProductName", type text}, {"Category", type text},
        {"UnitCostTND", type number}, {"UnitPriceTND", type number}, {"MarginTND", type number}
    })
in
    Typed

// ----- Query name: Dim_Payment ------------------------------------------------
let
    Source = Csv.Document(File.Contents("C:\Users\MSI\Desktop\New folder\baristas-coffee-analytics\data_generator\data\dim_payment.csv"),[Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers,{
        {"PaymentKey", Int64.Type}, {"PaymentMethod", type text}, {"PaymentType", type text}
    })
in
    Typed

// ----- Query name: Dim_Channel ------------------------------------------------
let
    Source = Csv.Document(File.Contents("C:\Users\MSI\Desktop\New folder\baristas-coffee-analytics\data_generator\data\dim_channel.csv"),[Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers,{
        {"ChannelKey", Int64.Type}, {"ChannelName", type text}, {"ChannelGroup", type text}
    })
in
    Typed
