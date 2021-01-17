from django.shortcuts import render
from .models import Product, Purchase
import pandas as pd


def chart_select_view(request):
    error_message = None
    df = None  # data frame

    product_df = pd.DataFrame(Product.objects.all().values())
    purchase_df = pd.DataFrame(Purchase.objects.all().values())
    product_df['product_id'] = product_df['id']

    if purchase_df.shape[0] > 0:
        df = pd.merge(purchase_df, product_df, on='product_id').drop(
            ['id_y', 'date_y'],
            axis=1
        ).rename({
            'id_x': 'id',
            'date_x': 'date'
        },
            axis=1
        )
        if request.method == 'POST':
            char_types = request.POST['sales']
            date_from = request.POST['date_from']
            date_to = request.POST['date_to']
            if not df.empty:
                df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
                df2 = df.groupby('date', as_index=False)[
                    'total_price'].agg('sum')
    else:
        error_message = 'No records found'

    context = {
        'error_message': error_message,
        'products': product_df.to_html(),
        'purchases': purchase_df.to_html(),
        'df': df.to_html() if not df.empty else None,
        'df2': df2.to_html(),
    }
    return render(request, 'products/main.html', context)
