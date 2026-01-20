from ziwei_calculator import calculate_ziwei_chart
try:
    result = calculate_ziwei_chart(
        lunar_year=1991,
        lunar_month=5,
        lunar_day=21,
        shichen=7,
        year_tiangan='辛',
        year_dizhi='未'
    )
    print("Success!")
except Exception as e:
    import traceback
    traceback.print_exc()
