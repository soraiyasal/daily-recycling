# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime
# import calendar


# # Set page config for wider layout
# st.set_page_config(layout="wide")

# def get_hotel_name(postcode):
#     mapping = {
#         'EC3N 1AX': 'Canopy',
#         'SW1V 1QF': 'CIV',
#         'W2 1EG': 'CIE',
#         'NW1 7BY': 'Camden',
#         'SW1V 1RG': 'EH',
#         'NW1 6UB': 'Head Office'
#     }
#     return mapping.get(postcode, 'Unknown')

# def get_status_color(rate):
#     if rate >= 50:
#         return "🟢 Excellent"
#     elif rate >= 40:
#         return "🟡 Good"
#     else:
#         return "🔴 Needs Improvement"


# def load_and_process_data(file):
#     df = pd.read_csv(file)
#     # Explicitly convert SERVICE DATE to datetime, handling any parsing errors
#     df['SERVICE DATE'] = pd.to_datetime(df['SERVICE DATE'].str.split('T').str[0])
#     df['Hotel'] = df['SITE POSTCODE'].apply(get_hotel_name)
#     df['Day of Week'] = df['SERVICE DATE'].dt.day_name()
#     df['Month'] = df['SERVICE DATE'].dt.strftime('%B')
#     return df

# def calculate_recycling_rate(subset_df):
#     subset_df = subset_df[subset_df['WEIGHT (TONNES)'].notna() & (subset_df['WEIGHT (TONNES)'] > 0)]
    
#     # Calculate recycling rate (including food waste in total)
#     recyclable = subset_df[subset_df['WASTE TYPE'].isin(['Mixed Recycling', 'Glass', 'Cardboard'])]['WEIGHT (TONNES)'].sum()
#     general = subset_df[subset_df['WASTE TYPE'] == 'General Waste']['WEIGHT (TONNES)'].sum()
#     food = subset_df[subset_df['WASTE TYPE'] == 'Food Waste']['WEIGHT (TONNES)'].sum()
    
#     total_waste = recyclable + general + food
#     recycling_rate = (recyclable / total_waste * 100) if total_waste > 0 else 0
    
#     return recycling_rate, food, total_waste

# def analyze_recycling(df, selected_hotel=None):
#     if selected_hotel and selected_hotel != 'All Hotels':
#         df = df[df['Hotel'] == selected_hotel]
    
#     df = df[df['WEIGHT (TONNES)'].notna() & (df['WEIGHT (TONNES)'] > 0)]
    
#     # Monthly analysis
#     monthly_rates = []
#     for month in df['Month'].unique():
#         month_data = df[df['Month'] == month]
#         rate, food, total = calculate_recycling_rate(month_data)
#         monthly_rates.append({
#             'Month': month,
#             'Recycling Rate': rate,
#             'Food Waste': food,
#             'Total Waste': total
#         })
#     monthly_rates = pd.DataFrame(monthly_rates)
    
#     # Daily analysis
#     daily_data = df.groupby(['SERVICE DATE', 'WASTE TYPE'])['WEIGHT (TONNES)'].sum().reset_index()
#     dates = daily_data['SERVICE DATE'].unique()
    
#     recycling_rates = []
#     for date in dates:
#         day_data = daily_data[daily_data['SERVICE DATE'] == date]
#         recyclable = day_data[day_data['WASTE TYPE'].isin(['Mixed Recycling', 'Glass', 'Cardboard'])]['WEIGHT (TONNES)'].sum()
#         general = day_data[day_data['WASTE TYPE'] == 'General Waste']['WEIGHT (TONNES)'].sum()
#         food = day_data[day_data['WASTE TYPE'] == 'Food Waste']['WEIGHT (TONNES)'].sum()
#         total = recyclable + general + food
        
#         if total > 0:
#             rate = (recyclable / total * 100)
#             recycling_rates.append({
#                 'date': date,
#                 'recycling_rate': rate,
#                 'recyclable': recyclable,
#                 'general': general,
#                 'food_waste': food,
#                 'total_waste': total
#             })
    
#     daily_df = pd.DataFrame(recycling_rates)
    
#     # Overall statistics
#     overall_rate, total_food, total_waste = calculate_recycling_rate(df)
    
#     # Day of week analysis
#     day_rates = []
#     for day in df['Day of Week'].unique():
#         day_data = df[df['Day of Week'] == day]
#         rate, food, total = calculate_recycling_rate(day_data)
#         day_rates.append({
#             'Day of Week': day,
#             'Recycling Rate': rate,
#             'Food Waste': food,
#             'Total Waste': total
#         })
#     day_rates = pd.DataFrame(day_rates)
#     day_rates = day_rates[day_rates['Total Waste'] > 0]
    
#     if not day_rates.empty:
#         best_day = day_rates.loc[day_rates['Recycling Rate'].idxmax()]
#         worst_day = day_rates.loc[day_rates['Recycling Rate'].idxmin()]
#     else:
#         best_day = {'Day of Week': 'No Data', 'Recycling Rate': 0}
#         worst_day = {'Day of Week': 'No Data', 'Recycling Rate': 0}
    
#     # Generate insights
#     insights = []
#     if not day_rates.empty:
#         avg_rate = day_rates['Recycling Rate'].mean()
#         low_days = day_rates[day_rates['Recycling Rate'] < avg_rate * 0.8]
        
#         for _, day in low_days.iterrows():
#             insights.append({
#                 'type': 'warning',
#                 'message': f"Low recycling rate on {day['Day of Week']}: {day['Recycling Rate']:.1f}%"
#             })
    
#     # Add food waste insights
#     avg_food_per_day = total_food / len(daily_df) if not daily_df.empty else 0
#     if avg_food_per_day > 0.2:  # Threshold can be adjusted
#         insights.append({
#             'type': 'info',
#             'message': f"High average food waste: {avg_food_per_day:.2f} tonnes per day"
#         })

#     return daily_df, overall_rate, best_day, worst_day, insights, day_rates, monthly_rates, total_food, total_waste

# def main():
# # At the top of your main() function, before the file uploader:
#     st.title('🌍 Hotel Recycling Performance Dashboard')

#     # Add instructions with GIF
#     st.markdown("""
#     ### How to Use This Dashboard
#     1. Download your waste report from the portal
#     2. Upload the CSV file below
#     3. Analyze your recycling performance
#     """)

#     # Display GIF in a smaller column
#     col1, col2, col3 = st.columns([1,2,1])
#     with col2:
#         st.image("download.gif", caption="How to download your waste report", use_column_width=True)

#     st.divider()  # Adds a visual separator

#     # Then continue with your existing file uploader
#     uploaded_file = st.file_uploader("📤 Upload your waste report CSV", type="csv")
    
#     if uploaded_file is not None:
#         df = load_and_process_data(uploaded_file)
        
#         hotels = ['All Hotels'] + sorted(df['Hotel'].unique().tolist())
#         selected_hotel = st.selectbox('🏨 Select Hotel:', hotels)
        
#         daily_data, overall_rate, best_day, worst_day, insights, day_rates, monthly_rates, total_food, total_waste = analyze_recycling(df, selected_hotel)
        
#         st.subheader("📊 Performance Overview")
#         status = get_status_color(overall_rate)
        
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             st.metric("Current Recycling Rate", f"{overall_rate:.1f}%")
#             st.markdown(f"Status: {status}")
#         with col2:
#             st.metric("Total Waste", f"{total_waste:.2f} tonnes")
#         with col3:
#             st.metric("Food Waste", f"{total_food:.2f} tonnes")
#         with col4:
#             food_waste_pct = (total_food/total_waste * 100) if total_waste > 0 else 0
#             st.metric("Food Waste %", f"{food_waste_pct:.1f}%")
        
#         st.subheader("🔍 Key Insights")
#         for insight in insights:
#             if insight['type'] == 'warning':
#                 st.warning(insight['message'])
#             elif insight['type'] == 'success':
#                 st.success(insight['message'])
#             else:
#                 st.info(insight['message'])
        
#         tab1, tab2, tab3 = st.tabs(["📈 Trends", "📅 Daily Performance", "📊 Waste Composition"])
        
#         with tab1:
#             if not daily_data.empty:
#                 st.subheader("Recycling Rate Trend")
#                 fig1 = px.line(daily_data, x='date', y='recycling_rate',
#                              title='Daily Recycling Rate',
#                              color_discrete_sequence=['#2ecc71'])
#                 fig1.update_layout(
#                     yaxis_title="Recycling Rate (%)",
#                     xaxis_title="Date"
#                 )
#                 st.plotly_chart(fig1, use_container_width=True)
        
#         with tab2:
#             if not day_rates.empty:
#                 st.subheader("Daily Performance")
#                 day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#                 day_rates['Day of Week'] = pd.Categorical(day_rates['Day of Week'], categories=day_order, ordered=True)
#                 day_rates = day_rates.sort_values('Day of Week')
                
#                 fig2 = px.bar(day_rates, x='Day of Week', y='Recycling Rate',
#                              title='Average Recycling Rate by Day',
#                              color='Recycling Rate',
#                              color_continuous_scale=['red', 'yellow', 'green'])
#                 st.plotly_chart(fig2, use_container_width=True)
        
#         with tab3:
#             if not daily_data.empty:
#                 st.subheader("Waste Composition")
#                 fig3 = go.Figure()
#                 fig3.add_bar(name='Recyclable', x=daily_data['date'], y=daily_data['recyclable'],
#                            marker_color='#2ecc71')
#                 fig3.add_bar(name='General Waste', x=daily_data['date'], y=daily_data['general'],
#                            marker_color='#e74c3c')
#                 fig3.add_bar(name='Food Waste', x=daily_data['date'], y=daily_data['food_waste'],
#                            marker_color='#f1c40f')
#                 fig3.update_layout(
#                     barmode='stack',
#                     title='Daily Waste Composition',
#                     yaxis_title="Weight (Tonnes)",
#                     xaxis_title="Date"
#                 )
#                 st.plotly_chart(fig3, use_container_width=True)
        
#         st.subheader("💡 Improvement Tips")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.markdown("""
#             ### Quick Wins
#             * 🗑️ Clear labeling on all waste bins
#             * 📝 Post waste segregation guides in key areas
#             * ⏰ Regular bin checks throughout the day
#             * 🎯 Daily waste segregation targets
#             * 🔍 Monitor food waste levels
#             """)
            
#         with col2:
#             st.markdown("""
#             ### Long-term Strategies
#             * 📊 Weekly waste audits
#             * 👥 Regular staff training on waste segregation
#             * 🏆 Recognition for good recycling practices
#             * 📈 Monthly improvement targets
#             * 🥘 Food waste reduction program
#             """)

# if __name__ == "__main__":
#     main()

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar

# Set page config for wider layout
st.set_page_config(layout="wide")

def get_hotel_name(postcode):
    mapping = {
        'EC3N 1AX': 'Canopy',
        'SW1V 1QF': 'CIV',
        'W2 1EG': 'CIE',
        'NW1 7BY': 'Camden',
        'SW1V 1RG': 'EH',
        'NW1 6UB': 'Head Office'
    }
    return mapping.get(postcode, 'Unknown')

def get_status_color(rate):
    if rate >= 50:
        return "🟢 Excellent"
    elif rate >= 40:
        return "🟡 Good"
    else:
        return "🔴 Needs Improvement"

def load_and_process_data(file):
    df = pd.read_csv(file)
    # Explicitly convert SERVICE DATE to datetime, handling any parsing errors
    df['SERVICE DATE'] = pd.to_datetime(df['SERVICE DATE'].str.split('T').str[0])
    df['Hotel'] = df['SITE POSTCODE'].apply(get_hotel_name)
    df['Day of Week'] = df['SERVICE DATE'].dt.day_name()
    df['Month'] = df['SERVICE DATE'].dt.strftime('%B')
    return df

def calculate_recycling_rate(subset_df):
    subset_df = subset_df[subset_df['WEIGHT (TONNES)'].notna() & (subset_df['WEIGHT (TONNES)'] > 0)]
    
    # Calculate recycling rate (including food waste in total)
    recyclable = subset_df[subset_df['WASTE TYPE'].isin(['Mixed Recycling', 'Glass', 'Cardboard'])]['WEIGHT (TONNES)'].sum()
    general = subset_df[subset_df['WASTE TYPE'] == 'General Waste']['WEIGHT (TONNES)'].sum()
    food = subset_df[subset_df['WASTE TYPE'] == 'Food Waste']['WEIGHT (TONNES)'].sum()
    
    total_waste = recyclable + general + food
    recycling_rate = (recyclable / total_waste * 100) if total_waste > 0 else 0
    
    return recycling_rate, food, total_waste

def analyze_recycling(df, selected_hotel=None):
    if selected_hotel and selected_hotel != 'All Hotels':
        df = df[df['Hotel'] == selected_hotel]
    
    df = df[df['WEIGHT (TONNES)'].notna() & (df['WEIGHT (TONNES)'] > 0)]
    
    # Add week number to the dataframe
    df['Week'] = df['SERVICE DATE'].dt.isocalendar().week
    
    # Calculate weekly rates by day
    weekly_daily_rates = []
    for week in df['Week'].unique():
        week_data = df[df['Week'] == week]
        # Get the start date of the week (first date in that week's data)
        week_start = week_data['SERVICE DATE'].min().strftime('%Y-%m-%d')
        for day in week_data['Day of Week'].unique():
            day_data = week_data[week_data['Day of Week'] == day]
            rate, food, total = calculate_recycling_rate(day_data)
            weekly_daily_rates.append({
                'Week': week,
                'Week Start': week_start,
                'Day of Week': day,
                'Recycling Rate': rate,
                'Food Waste': food,
                'Total Waste': total
            })

    
    weekly_daily_df = pd.DataFrame(weekly_daily_rates)
    
    # Monthly analysis
    monthly_rates = []
    for month in df['Month'].unique():
        month_data = df[df['Month'] == month]
        rate, food, total = calculate_recycling_rate(month_data)
        monthly_rates.append({
            'Month': month,
            'Recycling Rate': rate,
            'Food Waste': food,
            'Total Waste': total
        })
    monthly_rates = pd.DataFrame(monthly_rates)
    
    # Daily analysis
    daily_data = df.groupby(['SERVICE DATE', 'WASTE TYPE'])['WEIGHT (TONNES)'].sum().reset_index()
    dates = daily_data['SERVICE DATE'].unique()
    
    recycling_rates = []
    for date in dates:
        day_data = daily_data[daily_data['SERVICE DATE'] == date]
        recyclable = day_data[day_data['WASTE TYPE'].isin(['Mixed Recycling', 'Glass', 'Cardboard'])]['WEIGHT (TONNES)'].sum()
        general = day_data[day_data['WASTE TYPE'] == 'General Waste']['WEIGHT (TONNES)'].sum()
        food = day_data[day_data['WASTE TYPE'] == 'Food Waste']['WEIGHT (TONNES)'].sum()
        total = recyclable + general + food
        
        if total > 0:
            rate = (recyclable / total * 100)
            recycling_rates.append({
                'date': date,
                'recycling_rate': rate,
                'recyclable': recyclable,
                'general': general,
                'food_waste': food,
                'total_waste': total
            })
    
    daily_df = pd.DataFrame(recycling_rates)
    
    # Overall statistics
    overall_rate, total_food, total_waste = calculate_recycling_rate(df)
    
    # Day of week analysis
    day_rates = []
    for day in df['Day of Week'].unique():
        day_data = df[df['Day of Week'] == day]
        rate, food, total = calculate_recycling_rate(day_data)
        day_rates.append({
            'Day of Week': day,
            'Recycling Rate': rate,
            'Food Waste': food,
            'Total Waste': total
        })
    day_rates = pd.DataFrame(day_rates)
    day_rates = day_rates[day_rates['Total Waste'] > 0]
    
    if not day_rates.empty:
        best_day = day_rates.loc[day_rates['Recycling Rate'].idxmax()]
        worst_day = day_rates.loc[day_rates['Recycling Rate'].idxmin()]
    else:
        best_day = {'Day of Week': 'No Data', 'Recycling Rate': 0}
        worst_day = {'Day of Week': 'No Data', 'Recycling Rate': 0}
    
    # Generate insights
    insights = []
    if not day_rates.empty:
        avg_rate = day_rates['Recycling Rate'].mean()
        low_days = day_rates[day_rates['Recycling Rate'] < avg_rate * 0.8]
        
        for _, day in low_days.iterrows():
            insights.append({
                'type': 'warning',
                'message': f"Low recycling rate on {day['Day of Week']}: {day['Recycling Rate']:.1f}%"
            })
    
    # Add food waste insights
    avg_food_per_day = total_food / len(daily_df) if not daily_df.empty else 0
    if avg_food_per_day > 0.2:  # Threshold can be adjusted
        insights.append({
            'type': 'info',
            'message': f"High average food waste: {avg_food_per_day:.2f} tonnes per day"
        })

    return daily_df, overall_rate, best_day, worst_day, insights, day_rates, monthly_rates, total_food, total_waste, weekly_daily_df

def main():
    st.title('🌍 Hotel Recycling Performance Dashboard')

    # Add instructions with GIF
    st.markdown("""
    ### How to Use This Dashboard
    1. Download your waste report from the portal
    2. Upload the CSV file below
    3. Analyze your recycling performance
    """)

    # Display GIF in a smaller column
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("download.gif", caption="How to download your waste report", use_column_width=True)

    st.divider()  # Adds a visual separator

    uploaded_file = st.file_uploader("📤 Upload your waste report CSV", type="csv")
    
    if uploaded_file is not None:
        df = load_and_process_data(uploaded_file)
        
        hotels = ['All Hotels'] + sorted(df['Hotel'].unique().tolist())
        selected_hotel = st.selectbox('🏨 Select Hotel:', hotels)
        
        daily_data, overall_rate, best_day, worst_day, insights, day_rates, monthly_rates, total_food, total_waste, weekly_daily_df = analyze_recycling(df, selected_hotel)
        
        st.subheader("📊 Performance Overview")
        status = get_status_color(overall_rate)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Current Recycling Rate", f"{overall_rate:.1f}%")
            st.markdown(f"Status: {status}")
        with col2:
            st.metric("Total Waste", f"{total_waste:.2f} tonnes")
        with col3:
            st.metric("Food Waste", f"{total_food:.2f} tonnes")
        with col4:
            food_waste_pct = (total_food/total_waste * 100) if total_waste > 0 else 0
            st.metric("Food Waste %", f"{food_waste_pct:.1f}%")
        
        st.subheader("🔍 Key Insights")
        for insight in insights:
            if insight['type'] == 'warning':
                st.warning(insight['message'])
            elif insight['type'] == 'success':
                st.success(insight['message'])
            else:
                st.info(insight['message'])
        
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "📅 Daily Performance", "📊 Waste Composition", "📆 Weekly Analysis"])
        
        with tab1:
            if not daily_data.empty:
                st.subheader("Recycling Rate Trend")
                fig1 = px.line(daily_data, x='date', y='recycling_rate',
                             title='Daily Recycling Rate',
                             color_discrete_sequence=['#2ecc71'])
                fig1.update_layout(
                    yaxis_title="Recycling Rate (%)",
                    xaxis_title="Date"
                )
                st.plotly_chart(fig1, use_container_width=True)
        
        with tab2:
            if not day_rates.empty:
                st.subheader("Daily Performance")
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day_rates['Day of Week'] = pd.Categorical(day_rates['Day of Week'], categories=day_order, ordered=True)
                day_rates = day_rates.sort_values('Day of Week')
                
                fig2 = px.bar(day_rates, x='Day of Week', y='Recycling Rate',
                             title='Average Recycling Rate by Day',
                             color='Recycling Rate',
                             color_continuous_scale=['red', 'yellow', 'green'])
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab3:
            if not daily_data.empty:
                st.subheader("Waste Composition")
                fig3 = go.Figure()
                fig3.add_bar(name='Recyclable', x=daily_data['date'], y=daily_data['recyclable'],
                           marker_color='#2ecc71')
                fig3.add_bar(name='General Waste', x=daily_data['date'], y=daily_data['general'],
                           marker_color='#e74c3c')
                fig3.add_bar(name='Food Waste', x=daily_data['date'], y=daily_data['food_waste'],
                           marker_color='#f1c40f')
                fig3.update_layout(
                    barmode='stack',
                    title='Daily Waste Composition',
                    yaxis_title="Weight (Tonnes)",
                    xaxis_title="Date"
                )
                st.plotly_chart(fig3, use_container_width=True)
        
        with tab4:
            if not weekly_daily_df.empty:
                st.subheader("Weekly Performance by Day")
                
                # Create day order for consistent display
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                weekly_daily_df['Day of Week'] = pd.Categorical(weekly_daily_df['Day of Week'], 
                                                              categories=day_order, 
                                                              ordered=True)
                
                # Create line plot with multiple weeks
                fig4 = go.Figure()
                
                # Add a line for each week
                for week in weekly_daily_df['Week'].unique():
                    week_data = weekly_daily_df[weekly_daily_df['Week'] == week]
                    week_start = week_data['Week Start'].iloc[0]
                    week_data = week_data.sort_values('Day of Week')
                    
                    fig4.add_trace(go.Scatter(
                        x=week_data['Day of Week'],
                        y=week_data['Recycling Rate'],
                        mode='lines+markers',
                        name=f'Week c/o {week_start}',
                        hovertemplate="Week c/o %{text}<br>" +
                                    "Day: %{x}<br>" +
                                    "Recycling Rate: %{y:.1f}%<extra></extra>",
                        text=[week_start] * len(week_data)
                    ))
                
                # Add average line
                avg_by_day = weekly_daily_df.groupby('Day of Week')['Recycling Rate'].mean().reset_index()
                avg_by_day = avg_by_day.sort_values('Day of Week')
                
                fig4.add_trace(go.Scatter(
                    x=avg_by_day['Day of Week'],
                    y=avg_by_day['Recycling Rate'],
                    mode='lines+markers',
                    name='Average',
                    line=dict(color='black', width=3, dash='dash'),
                    hovertemplate="Average<br>" +
                                "Day: %{x}<br>" +
                                "Recycling Rate: %{y:.1f}%<extra></extra>"
                ))
                
                fig4.update_layout(
                    title='Recycling Rates by Day of Week (Weekly Comparison)',
                    xaxis_title='Day of Week',
                    yaxis_title='Recycling Rate (%)',
                    hovermode='x unified',
                    showlegend=True,
                    legend_title_text='Week Commencing'
                )
                
                st.plotly_chart(fig4, use_container_width=True)
                
                # Add summary statistics
                st.subheader("Day of Week Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Average Recycling Rate by Day")
                    avg_rates = avg_by_day.set_index('Day of Week')['Recycling Rate'].round(1)
                    for day, rate in avg_rates.items():
                        st.write(f"{day}: {rate}%")
                
                with col2:
                                    st.markdown("#### Consistency Analysis")
                                    std_by_day = weekly_daily_df.groupby('Day of Week')['Recycling Rate'].std().round(1)
                                    for day, std in std_by_day.items():
                                        consistency = "High" if std < 5 else "Medium" if std < 10 else "Low"
                                        st.write(f"{day}: {consistency} consistency (std: {std}%)")
                        
                st.subheader("💡 Improvement Tips")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    ### Quick Wins
                    * 🗑️ Clear labeling on all waste bins
                    * 📝 Post waste segregation guides in key areas
                    * ⏰ Regular bin checks throughout the day
                    * 🎯 Daily waste segregation targets
                    * 🔍 Monitor food waste levels
                    """)
                    
                with col2:
                    st.markdown("""
                    ### Long-term Strategies
                    * 📊 Weekly waste audits
                    * 👥 Regular staff training on waste segregation
                    * 🏆 Recognition for good recycling practices
                    * 📈 Monthly improvement targets
                    * 🥘 Food waste reduction program
                    """)

if __name__ == "__main__":
    main()