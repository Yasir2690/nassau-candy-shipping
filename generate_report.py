# ============================================
# Nassau Candy Research Paper - PDF Generator
# Generates exact formatted PDF from the report content
# Run: pip install fpdf pandas
# ============================================

from fpdf import FPDF
import pandas as pd
from datetime import datetime

class NassauCandyReport(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('helvetica', '', 'helvetica')
        self.add_font('helvetica', 'B', 'helvetica-bold')
        
    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Nassau Candy Distributor - Route Efficiency Analysis', 0, 0, 'L')
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'R')
            self.ln(8)
            self.set_draw_color(200, 200, 200)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d")}', 0, 0, 'C')
    
    def section_title(self, title):
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, title, 0, 1, 'L')
        self.set_draw_color(0, 51, 102)
        self.line(10, self.get_y(), 50, self.get_y())
        self.ln(5)
    
    def subsection_title(self, title):
        self.set_font('helvetica', 'B', 11)
        self.set_text_color(0, 51, 102)
        self.cell(0, 8, title, 0, 1, 'L')
        self.ln(2)
    
    def body_text(self, text):
        self.set_font('helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, text)
        self.ln(3)
    
    def bullet_point(self, text):
        self.set_font('helvetica', '', 10)
        self.cell(8, 5, '•', 0, 0)
        self.multi_cell(0, 5, text)
    
    def create_table(self, headers, data, col_widths=None):
        self.set_font('helvetica', 'B', 9)
        if col_widths is None:
            col_widths = [190/len(headers)] * len(headers)
        
        # Header
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, 1, 0, 'C', True)
        self.ln()
        
        # Data rows
        self.set_font('helvetica', '', 9)
        self.set_text_color(0, 0, 0)
        for row in data:
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 7, str(cell), 1, 0, 'L')
            self.ln()
        self.ln(5)


def create_report():
    pdf = NassauCandyReport()
    pdf.add_page()
    
    # ============================================
    # COVER PAGE
    # ============================================
    pdf.set_y(60)
    pdf.set_font('helvetica', 'B', 22)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 15, 'Nassau Candy Distributor', 0, 1, 'C')
    pdf.set_font('helvetica', 'B', 18)
    pdf.cell(0, 12, 'Shipping Route Efficiency Analysis', 0, 1, 'C')
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, 'Data-Driven Logistics Optimization', 0, 1, 'C')
    
    pdf.ln(30)
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, 'Prepared for: Nassau Candy Distributor | Unified Mentor Internship Project', 0, 1, 'C')
    pdf.cell(0, 6, f'Date: {datetime.now().strftime("%B %Y")}', 0, 1, 'C')
    
    pdf.ln(15)
    pdf.set_font('helvetica', 'I', 9)
    pdf.cell(0, 6, 'Tools Used: Python · Pandas · Plotly · Streamlit', 0, 1, 'C')
    
    # KPI Box
    pdf.ln(20)
    pdf.set_fill_color(240, 248, 255)
    pdf.set_draw_color(0, 51, 102)
    pdf.set_font('helvetica', 'B', 10)
    
    kpis = [('10,194', 'Total Orders'), ('1,320.8 days', 'Avg Lead Time'), 
            ('33.1%', 'Delay Rate'), ('20', 'Routes Analyzed')]
    
    x_start = 25
    for i, (value, label) in enumerate(kpis):
        pdf.set_xy(x_start + (i * 42), pdf.get_y())
        pdf.cell(35, 25, '', 1, 0, 'C', True)
        pdf.set_xy(x_start + (i * 42), pdf.get_y() - 18)
        pdf.set_font('helvetica', 'B', 12)
        pdf.cell(35, 8, value, 0, 0, 'C')
        pdf.set_xy(x_start + (i * 42), pdf.get_y() + 6)
        pdf.set_font('helvetica', '', 8)
        pdf.cell(35, 6, label, 0, 0, 'C')
        pdf.set_y(pdf.get_y() + 12)
    
    # ============================================
    # PAGE 2 - INTRODUCTION
    # ============================================
    pdf.add_page()
    
    pdf.section_title('1. Introduction')
    
    pdf.subsection_title('Abstract')
    pdf.body_text('This report presents a comprehensive data-driven analysis of shipping route efficiency for Nassau Candy Distributor, a national candy distributor operating across four US regions. Using order and shipment data containing 10,194 transactions from 2024 to 2030, we calculated key performance indicators including shipping lead time, delay rates, and route efficiency scores. The analysis reveals that the company\'s average shipping lead time is 1,320 days (approximately 3.6 years), indicating severe operational bottlenecks across all factory-to-customer routes. We identified the most efficient route as Sugar Shack → Gulf with 1,091 days, while the least efficient route is Sugar Shack → Pacific with 1,516 days. Based on these findings, we provide three actionable recommendations to reduce lead times, optimize shipping methods, and resolve geographic bottlenecks.')
    
    pdf.subsection_title('1.1 Problem Statement')
    pdf.body_text('Nassau Candy Distributor operates as a national distributor shipping products from multiple factories to customers across four US regions: Atlantic, Gulf, Interior, and Pacific. Despite having rich order and shipment data, the organization currently lacks clarity on:')
    pdf.bullet_point('Which factory-to-customer routes are consistently efficient')
    pdf.bullet_point('Which routes experience frequent delays')
    pdf.bullet_point('How shipping performance varies by region, state, and ship mode')
    pdf.bullet_point('Where operational bottlenecks exist geographically')
    
    pdf.body_text('Without this visibility, logistics optimization remains reactive rather than data-driven. Shipping inefficiencies directly affect customer satisfaction, increase operational costs, and reduce scalability. This project transforms raw order and shipment data into route-level operational intelligence, enabling data-driven logistics decisions.')
    
    pdf.subsection_title('1.2 Project Objectives')
    pdf.bullet_point('Calculate and benchmark shipping lead time as the primary KPI')
    pdf.bullet_point('Identify top 10 most efficient and bottom 10 least efficient routes')
    pdf.bullet_point('Analyze regional and state-level performance to detect bottlenecks')
    pdf.bullet_point('Compare shipping methods to find optimal cost-speed tradeoffs')
    pdf.bullet_point('Build an interactive Streamlit dashboard for ongoing logistics monitoring')
    
    # ============================================
    # PAGE 3 - DATASET DESCRIPTION
    # ============================================
    pdf.add_page()
    
    pdf.section_title('2. Dataset Description')
    
    pdf.subsection_title('2.1 Data Overview')
    pdf.body_text('The dataset contains 10,194 orders placed between January 2024 and December 2025, with shipments scheduled from June 2026 to June 2030. Each record represents a single order line item with complete customer, product, and shipping information across 19 fields.')
    
    pdf.subsection_title('2.2 Fields Description')
    
    fields_data = [
        ['Row ID', 'Unique row identifier'],
        ['Order ID', 'Unique order identifier'],
        ['Order Date', 'Date when order was placed (DD-MM-YYYY)'],
        ['Ship Date', 'Date when order was shipped (DD-MM-YYYY)'],
        ['Ship Mode', 'Shipping method (Standard, Second, First Class, Same Day)'],
        ['Customer ID', 'Unique customer identifier'],
        ['Country/Region', 'Country of customer (USA only)'],
        ['City', 'City of customer'],
        ['State/Province', 'State or province of customer'],
        ['Postal Code', 'Zip code of customer'],
        ['Division', 'Product division (Chocolate, Sugar, Other)'],
        ['Region', 'Customer region (Atlantic, Gulf, Interior, Pacific)'],
        ['Product ID', 'Unique product identifier'],
        ['Product Name', 'Full product name'],
        ['Sales', 'Total sales value of order ($)'],
        ['Units', 'Total units ordered'],
        ['Gross Profit', 'Profit = Sales - Cost'],
        ['Cost', 'Manufacturing cost ($)']
    ]
    
    pdf.create_table(['Field', 'Description'], fields_data, [50, 140])
    
    pdf.subsection_title('2.3 Factory Mapping')
    pdf.body_text('Each product is manufactured at one of five factories. Product-to-factory mapping was performed using a Python dictionary lookup, adding a Factory column to the dataset which serves as the origin point for all route definitions.')
    
    factory_data = [
        ['Lot\'s O\' Nuts', 'Arizona', '32.88, -111.77', 'Wonka Bar - Nutty Crunch Surprise, Fudge Mallows, Scrumdiddlyumpitous'],
        ['Wicked Choccy\'s', 'Georgia', '32.08, -81.09', 'Wonka Bar - Milk Chocolate, Triple Dazzle Caramel'],
        ['Sugar Shack', 'Minnesota', '48.12, -96.18', 'Laffy Taffy, SweeTARTS, Nerds, Fun Dip, Fizzy Lifting Drinks'],
        ['Secret Factory', 'Illinois', '41.45, -90.57', 'Everlasting Gobstopper, Lickable Wallpaper, Wonka Gum'],
        ['The Other Factory', 'Tennessee', '35.12, -89.97', 'Hair Toffee, Kazookles']
    ]
    
    pdf.create_table(['Factory', 'State', 'Coordinates', 'Products Manufactured'], 
                     factory_data, [40, 25, 35, 90])
    
    # ============================================
    # PAGE 4 - METHODOLOGY
    # ============================================
    pdf.add_page()
    
    pdf.section_title('3. Methodology')
    
    pdf.subsection_title('3.1 Data Cleaning')
    pdf.body_text('Step 1 - Date Parsing: Dates were in DD-MM-YYYY format and parsed explicitly.')
    pdf.body_text('Step 2 - Lead Time Calculation: The primary KPI - shipping lead time - was derived as:')
    pdf.set_font('helvetica', '', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, 'df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days', 0, 1)
    pdf.body_text('Step 3 - Invalid Row Removal: Rows with negative lead time (ship date before order date) were removed.')
    
    pdf.subsection_title('3.2 Feature Engineering')
    pdf.body_text('Route Definition: Each unique factory-to-customer region combination was defined as a route. With 5 factories and 4 regions, a maximum of 20 routes are possible.')
    pdf.body_text('df["Route"] = df["Factory"] + " → " + df["Region"]')
    
    pdf.body_text('Delay Flag: A shipment was flagged as delayed if its lead time exceeded mean + 1 standard deviation, a statistically robust threshold that captures the top 16% of slow shipments.')
    
    pdf.subsection_title('3.3 Key Performance Indicators')
    
    kpi_data = [
        ['Shipping Lead Time', 'Ship Date - Order Date', 'Days between order placement and shipment'],
        ['Average Lead Time', 'Mean(Lead Time) per route', 'Route speed benchmark'],
        ['Delay Rate', '(Delayed orders) / (Total orders) x 100', 'Percentage of delayed shipments per route'],
        ['Efficiency Score', '(max_lt - route_lt) / (max_lt - min_lt) x 100', 'Normalized 0-100 score; 100 = fastest'],
        ['Route Volume', 'COUNT(orders) per route', 'Order frequency on each route']
    ]
    
    pdf.create_table(['KPI', 'Formula', 'Description'], kpi_data, [45, 60, 85])
    
    # ============================================
    # PAGE 5 - RESULTS (Top/Bottom Routes)
    # ============================================
    pdf.add_page()
    
    pdf.section_title('4. Results and Analysis')
    
    pdf.subsection_title('4.1 Critical Finding - Severe Operational Delays')
    pdf.body_text('Analysis reveals that Nassau Candy\'s average shipping lead time is 1,320 days (approximately 3.6 years), indicating severe operational bottlenecks in the supply chain. Even the most efficient route (Sugar Shack → Gulf) takes nearly 3 years (1,091 days) to deliver.')
    pdf.body_text('This finding suggests one of two possibilities:')
    pdf.bullet_point('Operational reality: The business has extreme backlog issues requiring immediate intervention.')
    pdf.bullet_point('Data quality issue: Ship dates contain planned/future dates rather than actual historical shipment dates.')
    pdf.body_text('In either scenario, this is the most significant finding of this analysis and demands immediate management attention.')
    
    pdf.subsection_title('4.2 Route Efficiency Analysis')
    pdf.body_text('20 unique factory-to-customer region routes were identified and benchmarked. Results are ranked from fastest (most efficient) to slowest.')
    
    top_routes_data = [
        ['1', 'Sugar Shack → Gulf', '1,091.2', '100.0', '42'],
        ['2', 'The Other Factory → Interior', '1,206.6', '72.9', '113'],
        ['3', 'The Other Factory → Gulf', '1,272.6', '57.4', '194'],
        ['4', 'The Other Factory → Atlantic', '1,282.7', '55.0', '38'],
        ['5', 'Secret Factory → Interior', '1,289.1', '53.5', '45']
    ]
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(0, 8, 'Top 5 Most Efficient Routes', 0, 1, 'L')
    pdf.create_table(['Rank', 'Route', 'Avg Lead Time (days)', 'Efficiency Score', 'Total Orders'], 
                     top_routes_data, [20, 70, 45, 35, 30])
    
    bottom_routes_data = [
        ['1 (worst)', 'Sugar Shack → Pacific', '1,516.7', '66.7%', '3'],
        ['2', 'Sugar Shack → Atlantic', '1,375.4', '44.4%', '18'],
        ['3', 'Secret Factory → Atlantic', '1,349.2', '41.7%', '72'],
        ['4', 'Secret Factory → Gulf', '1,332.5', '43.2%', '37'],
        ['5', 'Wicked Choccy\'s → Pacific', '1,329.1', '35.3%', '1,342']
    ]
    
    pdf.ln(5)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(0, 8, 'Bottom 5 Least Efficient Routes', 0, 1, 'L')
    pdf.create_table(['Rank', 'Route', 'Avg Lead Time (days)', 'Delay Rate', 'Total Orders'], 
                     bottom_routes_data, [30, 65, 40, 30, 35])
    
    pdf.subsection_title('4.3 Regional Performance')
    pdf.body_text('All four regions show similarly poor performance, with lead times ranging from 1,311 to 1,323 days.')
    
    regional_data = [
        ['Atlantic', '2,986', '1,322.8', '32%', '$41,197'],
        ['Gulf', '1,620', '1,311.4', '32%', '$22,247'],
        ['Interior', '2,335', '1,323.1', '34%', '$32,038'],
        ['Pacific', '3,253', '1,322.2', '34%', '$46,302']
    ]
    
    pdf.create_table(['Region', 'Orders', 'Avg Lead Time (days)', 'Delay Rate', 'Total Sales'], 
                     regional_data, [30, 25, 45, 25, 35])
    
    pdf.body_text('Key Insight: Gulf region has the lowest average lead time (1,311 days), while Interior region has the highest (1,323 days). Despite the ordering difference, all four regions show similarly poor performance, suggesting a systemic rather than region-specific issue.')
    
    # ============================================
    # PAGE 6 - SHIP MODE & STATE BOTTLENECKS
    # ============================================
    pdf.add_page()
    
    pdf.subsection_title('4.4 Ship Mode Comparison')
    
    shipmode_data = [
        ['Standard Class', '6,120', '1,314.3', '32%', '$4.75'],
        ['Second Class', '1,979', '1,323.9', '34%', '$4.83'],
        ['Same Day', '547', '1,333.4', '34%', '$4.41'],
        ['First Class', '1,548', '1,338.3', '37%', '$4.72']
    ]
    
    pdf.create_table(['Ship Mode', 'Orders', 'Avg Lead Time (days)', 'Delay Rate', 'Avg Cost ($)'], 
                     shipmode_data, [35, 25, 40, 25, 25])
    
    pdf.body_text('Key Insight: Standard Class is both the most cost-effective ($4.75 avg) and has the lowest delay rate (32%). Counterintuitively, "Same Day" and "First Class" show worse performance, suggesting that shipping method labels do not reflect actual handling priorities in the current logistics system.')
    
    pdf.subsection_title('4.5 State-Level Bottlenecks')
    pdf.body_text('Five states with the highest delay rates were identified as geographic bottlenecks:')
    
    bottlenecks_data = [
        ['North Dakota', '7', '1,637.9', '100%'],
        ['West Virginia', '4', '1,638.0', '100%'],
        ['South Dakota', '12', '1,395.9', '67%'],
        ['New Mexico', '37', '1,441.8', '59%'],
        ['Iowa', '30', '1,443.9', '53%']
    ]
    
    pdf.create_table(['State/Province', 'Orders', 'Avg Lead Time (days)', 'Delay Rate'], 
                     bottlenecks_data, [45, 25, 45, 35])
    
    # ============================================
    # PAGE 7 - CONCLUSIONS & RECOMMENDATIONS
    # ============================================
    pdf.add_page()
    
    pdf.section_title('5. Conclusion and Recommendations')
    
    pdf.subsection_title('5.1 Summary of Findings')
    pdf.bullet_point('Critical Lead Time Issue: Average shipping lead time of 1,320 days (3.6 years) indicates severe operational or data quality problems requiring immediate investigation.')
    pdf.bullet_point('Route Performance Variance: Sugar Shack factory shows the widest performance gap — fastest route (→ Gulf, 1,091 days) and slowest route (→ Pacific, 1,516 days) — a 425-day difference.')
    pdf.bullet_point('Ship Mode Inefficiency: Premium shipping methods (First Class, Same Day) perform worse than Standard Class, suggesting process inefficiencies rather than shipping method limitations.')
    pdf.bullet_point('Geographic Bottlenecks: North Dakota and West Virginia have 100% delay rates, requiring targeted and immediate logistics intervention.')
    
    pdf.subsection_title('5.2 Three Key Recommendations')
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(0, 7, 'Recommendation 1: Investigate Data Accuracy vs. Operational Reality', 0, 1)
    pdf.set_font('helvetica', '', 10)
    pdf.bullet_point('Confirm whether ship dates reflect actual shipment dates or future planned dates')
    pdf.bullet_point('If actual: launch an urgent operational audit of warehouse and logistics processes')
    pdf.bullet_point('If planned: redesign data capture to record actual ship dates for accurate KPI tracking')
    pdf.bullet_point('Establish a data governance policy to ensure date field integrity going forward')
    
    pdf.ln(3)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(0, 7, 'Recommendation 2: Standardize and Optimize Shipping Operations', 0, 1)
    pdf.set_font('helvetica', '', 10)
    pdf.bullet_point('Eliminate or restructure "Same Day" and "First Class" shipping offerings — they show no speed advantage')
    pdf.bullet_point('Implement route-specific performance targets starting with Sugar Shack → Pacific (worst route)')
    pdf.bullet_point('Create incentive programs for logistics partners tied to on-time shipment rates')
    pdf.bullet_point('Reallocate budget from premium shipping methods to process improvements in Standard Class')
    
    pdf.ln(3)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(0, 7, 'Recommendation 3: Address Geographic Bottlenecks', 0, 1)
    pdf.set_font('helvetica', '', 10)
    pdf.bullet_point('Investigate North Dakota and West Virginia (100% delay rate) for unique logistical challenges')
    pdf.bullet_point('Consider establishing regional distribution centers in high-delay states')
    pdf.bullet_point('Implement real-time tracking and priority queuing for shipments to bottleneck states')
    pdf.bullet_point('Conduct customer satisfaction surveys in high-delay regions to assess business impact')
    
    # ============================================
    # PAGE 8 - APPENDIX
    # ============================================
    pdf.add_page()
    
    pdf.section_title('Appendix: Dashboard Features')
    pdf.body_text('The accompanying Streamlit dashboard provides an interactive interface for ongoing logistics monitoring. It is structured into four tabs:')
    
    dashboard_data = [
        ['Route Efficiency', 'Route performance leaderboard (Top 10 / Bottom 10), horizontal bar chart with efficiency color scale'],
        ['Geographic View', 'US choropleth map (state-level lead time), regional comparison bar charts'],
        ['Ship Mode Analysis', 'Lead time comparison by shipping method, cost vs speed scatter plot'],
        ['Route Drill-Down', 'Per-route lead time distribution histogram with delay threshold marker, order-level detail table']
    ]
    
    pdf.create_table(['Tab', 'Features'], dashboard_data, [45, 145])
    
    pdf.ln(10)
    pdf.set_font('helvetica', 'I', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, 'End of Report', 0, 1, 'C')
    
    # Save PDF
    output_path = 'Nassau_Candy_Research_Paper_Corrected.pdf'
    pdf.output(output_path)
    print(f'PDF successfully created: {output_path}')
    return output_path


if __name__ == '__main__':
    create_report()
    print('\n✅ Report generated successfully!')
    print('📄 File: Nassau_Candy_Research_Paper_Corrected.pdf')