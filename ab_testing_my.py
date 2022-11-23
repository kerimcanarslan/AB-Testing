import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


## GÖREV 1 ( VERİYİ HAZIRLAMA VE ANALİZ ETME )

# ADIM 1
df_control = pd.read_excel("ab_testing/ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("ab_testing/ab_testing.xlsx", sheet_name="Test Group")

df_control.columns = ["Impression_cont", "Click_cont", "Purchase_cont", "Earning_cont"]
df_test.columns = ["Impression_test", "Click_test", "Purchase_test", "Earning_test"]


# ADIM 2

df_control.describe().T
df_test.describe().T



# ADIM 3

df = pd.concat([df_control, df_test], axis=1)



# GÖREV 2 ( Hipotez Tanımlama)

###########################
# 1. Hipotezi Kur
###########################

# H0: M1 = M2    ( iki durumdada satınalma sayısında istatistiksel bir fark yoktur )
# H1: M1 != M2   ( .... vardır )

############################
# 2. Varsayım Kontrolü
############################

# Normallik Varsayımı
# Varyans Homojenliği

                 ############################
                 # Normallik Varsayımı
                 ############################

                 # H0: Normal dağılım varsayımı sağlanmaktadır.
                 # H1:..sağlanmamaktadır.


test_stat, pvalue = shapiro(df["Purchase_cont"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 0.9773, p-value = 0.5891 > 0.05 olduğu için H0 reddeilemez.
# Yani Normal Dağılım varsayımı sağlanmaktadır

test_stat, pvalue = shapiro(df["Purchase_test"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 0.9589, p-value = 0.1541 > 0.05 olduğu için H0 reddeilemez.
# Yani Normal Dağılım varsayımı sağlanmaktadır

# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.


                 ############################
                 # Varyans Homojenliği Varsayımı
                 ############################

                 # H0: Varyanslar Homojendir
                 # H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(df["Purchase_cont"],
                           df["Purchase_test"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 2.6393, p-value = 0.1083 > 0.05 olduğu H0 reddedilemez
# Yani Varyanslar homojendir.


############################
# 3 ve 4. Hipotezin Uygulanması
############################

# 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
# 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)

############################
# 1.1 Varsayımlar sağlandığı için bağımsız iki örneklem t testi (parametrik test) yapacağız.
############################

test_stat, pvalue = ttest_ind(df["Purchase_cont"],
                              df["Purchase_test"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 2.6393, p-value = 0.3493 > 0.05 olduğu için H0 reddedilemez



####### Sonuçları analiz edecek olursak

# Maximum Bidding ve Average Bidding durumlarına göre iki senaryoda da Purchase olma durumunda
# istatistiksel oalrak anlamlı bir fark bulunmamktadır. Fakat elde edilen kazanç durumuna göre senaryoları tekrar
# gözden geçirmek istiyorum.



###########################
# 1. Hipotezi Kur
###########################

# H0: M1 = M2    ( iki durumdada Kazanç durumunda istatistiksel bir fark yoktur )
# H1: M1 != M2   ( .... vardır )

############################
# 2. Varsayım Kontrolü
############################

# Normallik Varsayımı
# Varyans Homojenliği

                 ############################
                 # Normallik Varsayımı
                 ############################

                 # H0: Normal dağılım varsayımı sağlanmaktadır.
                 # H1:..sağlanmamaktadır.

test_stat, pvalue = shapiro(df["Earning_cont"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 0.9756, p-value = 0.5306 > 0.05 olduğu için H0 reddedilemez.
# Yani Normal Dağılım varsayımı sağlanmaktadır

test_stat, pvalue = shapiro(df["Earning_test"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 0.9780, p-value = 0.6163 > 0.05 olduğu için H0 reddedilemez.
# Yani Normal Dağılım varsayımı sağlanmaktadır

                 ############################
                 # Varyans Homojenliği Varsayımı
                 ############################

                 # H0: Varyanslar Homojendir
                 # H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(df["Earning_cont"],
                           df["Earning_test"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 0.3532, p-value = 0.5540 > 0.05 olduğu H0 reddedilemez
# Yani Varyanslar homojendir.


############################
# 3 ve 4. Hipotezin Uygulanması
############################

# 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
# 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)

############################
# 1.1 Varsayımlar sağlandığı için bağımsız iki örneklem t testi (parametrik test) yapacağız.
############################

test_stat, pvalue = ttest_ind(df["Earning_cont"],
                              df["Earning_test"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = -9.2545, p-value = 0.0000 < 0.05 olduğu için H0 reddedilir.
# Yani elde edilen kazanç durumuna göre 2 senaryo arasında istatistiksel
# olarak anlamlı bir fark vardır. şimdi tekrar bakalım.

df[["Earning_cont", "Earning_test"]].mean()
df[["Earning_cont", "Earning_test"]].median()
# ortalamalar arasında bir fark var. Test senaryosunda daha çok para kazanmışız.
df[["Earning_cont", "Earning_test"]].sum()

df[["Impression_cont", "Impression_test"]].mean()

df[["Impression_cont", "Impression_test"]].sum()


# İki durumu da tekrar değerlendirince müşterimize şöyle bir yorum yapabilrim

# Test senaryosunda bize daha çok para kazandırabilecek müşterileri buluyor olabiliriz.
# satın alma sayılarında anlamlı bir fark yok, fakat satın alan kişilerin harcadığı parada
# anlamlı bir fark bulunuyor. Bu yüzden Test senaryosundan devam etmenizi tavsiye ederim.


# Ekstra; Firma Reklam tıklama başına ücret ödüyorsa, Tıklayan müşterilerin satın alma oranları
# bize anlamlı analizler yapmamızı sağlar
# bununiçin tutma oranı adında bir değişken oluşturalım

df_control["tutma_oranı_cont"] = (df_control["Purchase_cont"] / df_control["Click_cont"]) * 100
df_test["tutma_oranı_test"] = (df_test["Purchase_test"] / df_test["Click_test"]) * 100


df = pd.concat([df_control, df_test], axis=1)

df[["tutma_oranı_cont", "tutma_oranı_test"]].mean()

###########################
# 1. Hipotezi Kur
###########################

# H0: M1 = M2    ( iki durumdada müşteriyi tutma durumunda istatistiksel bir fark yoktur )
# H1: M1 != M2   ( .... vardır )

############################
# 2. Varsayım Kontrolü
############################

# Normallik Varsayımı
# Varyans Homojenliği

                 ############################
                 # Normallik Varsayımı
                 ############################

                 # H0: Normal dağılım varsayımı sağlanmaktadır.
                 # H1:..sağlanmamaktadır.

test_stat, pvalue = shapiro(df["tutma_oranı_cont"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 0.8720, p-value = 0.0003 < 0.05 olduğu için H0 reddedilir.
# Yani Normal Dağılım varsayımını kabul edemiyıoruz. Normal dağılmamışlar.

test_stat, pvalue = shapiro(df["tutma_oranı_test"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 0.8381, p-value = 0.0000 < 0.05 olduğu için H0 reddedilir.
# Yani Normal Dağılım varsayımını kabul edemiyıoruz. Normal dağılmamışlar.

                 ############################
                 # Varyans Homojenliği Varsayımı
                 ############################

                 # H0: Varyanslar Homojendir
                 # H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(df["tutma_oranı_cont"],
                           df["tutma_oranı_test"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 2.0759, p-value = 0.1536 > 0.05 olduğu H0 reddedilemez
# Yani Varyanslar homojendir.


############################
# 3 ve 4. Hipotezin Uygulanması
############################

# 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
# 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)

############################
# 1.2 Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
############################

test_stat, pvalue = mannwhitneyu(df["tutma_oranı_cont"],
                                 df["tutma_oranı_test"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 459.0000, p-value = 0.0011 < 0.05 olduğu H0 reddedilir.
# Yani tutma oranı karşılaştırılınca aralarında istatistiksel olarak anlamlı bir fark vardır.

df[["tutma_oranı_cont", "tutma_oranı_test"]].mean()

# Bu durumdada da test senaryosu müşterimiz için daha iyi olabilir, diyebilriiz.

