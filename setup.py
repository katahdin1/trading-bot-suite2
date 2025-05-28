from setuptools import setup, find_packages

setup(
    name='trading_bot_suite',
    version='1.0.0',
    author='Nickolaas Kriek',
    description='Automated Trading Bot Suite with strategy simulation, reports, Telegram/email alerts, and ML optimization',
    packages=find_packages(),
    install_requires=[
        'yfinance',
        'pandas',
        'numpy',
        'requests',
        'fpdf',
        'matplotlib',
        'schedule',
        'python-dotenv'
    ],
    include_package_data=True,
    python_requires='>=3.8',
)
