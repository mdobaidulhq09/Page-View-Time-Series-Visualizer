import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# date কলামকে datetime হিসেবে parse করে CSV পড়ছি
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# খুব ছোট আর খুব বড় মান বাদ দিচ্ছি
low = df['value'].quantile(0.025)
high = df['value'].quantile(0.975)
df = df[(df['value'] >= low) & (df['value'] <= high)]


def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15, 5))

    ax.plot(df.index, df['value'], color='red')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # নতুন কলাম বানাচ্ছি
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # year আর month অনুযায়ী average বের করছি
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # month number কে month name দিচ্ছি
    df_bar.columns = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    fig = df_bar.plot(kind='bar', figsize=(10, 8)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')

    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # box plot-এর জন্য data prepare করছি
    df_box = df.copy().reset_index()
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    fig, axes = plt.subplots(1, 2, figsize=(20, 6))

    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    fig.savefig('box_plot.png')
    return fig