library(foreign)
library(tidyr)
library(dplyr)
library(ggplot2)


sum_agri_by_cat <- function(cat) {
  kk <- summarize_agri %>% filter(from==cat)
  sum(kk$sum_area)
}

sum_urb_by_cat <- function(cat) {
  kk <- summarize_urb %>% filter(from==cat)
  sum(kk$sum_area)
}

sum_selva_by_cat <- function(cat) {
  kk <- summarize_selva %>% filter(from==cat)
  sum(kk$sum_area)
}

df1 <- read.dbf("C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/result/agro_s1_s3_new_patches_result.dbf")
df2 <- read.dbf("C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/result/agro_s3_s5_new_patches_result.dbf")

df4 <- read.dbf("C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/result/urb_s1_s3_new_patches_result.dbf")
df5 <- read.dbf("C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/result/urb_s3_s5_new_patches_result.dbf")

df7 <- read.dbf("C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/result/selva_s1_s3_new_patches_result.dbf")
df8 <- read.dbf("C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/result/selva_s3_s5_new_patches_result.dbf")


df1$year <- 2002
df1$prev_year <- 1985
df4$year <- 2002
df4$prev_year <- 1985
df7$year <- 2002
df7$prev_year <- 1985

df2$year <- 2011
df2$prev_year <- 2002
df5$year <- 2011
df5$prev_year <- 2002
df8$year <- 2011
df8$prev_year <- 2002


df1$area_year <- df1$area/(0.0+(df1$year - df1$prev_year))
df2$area_year <- df2$area/(0.0+(df2$year - df2$prev_year))

df4$area_year <- df4$area/(0.0+(df4$year - df4$prev_year))
df5$area_year <- df5$area/(0.0+(df5$year - df5$prev_year))

df7$area_year <- df7$area/(0.0+(df7$year - df7$prev_year))
df8$area_year <- df8$area/(0.0+(df8$year - df8$prev_year))

df_agri <- rbind(df1, df2)
df_urb <- rbind(df4, df5)
df_selva <- rbind(df7, df8)

summarize_agri <- df_agri %>% group_by(from,expander) %>% summarize(mean_area_year = mean(area_year),
                                                                    var_area_year = var(area_year),
                                                                    sum_area = sum(area))

#sum_agri_by_cat(9)

summarize_agri$area_cat <- mapply(sum_agri_by_cat, summarize_agri$from)

summarize_urb <- df_urb %>% group_by(from,expander) %>% summarize(mean_area_year = mean(area_year),
                                                                  var_area_year = var(area_year),
                                                                  sum_area = sum(area))
                                                               
summarize_urb$area_cat <- mapply(sum_urb_by_cat, summarize_urb$from)

summarize_selva <- df_selva %>% group_by(from,expander) %>% summarize(mean_area_year = mean(area_year),
                                                                    var_area_year = var(area_year),
                                                                    sum_area = sum(area))

#sum_agri_by_cat(9)

summarize_selva$area_cat <- mapply(sum_selva_by_cat, summarize_selva$from)

modulate_tm_agri <- summarize_agri %>% filter(expander==1)
modulate_tm_agri$to <- 2
modulate_tm_urb <- summarize_urb %>% filter(expander==1)
modulate_tm_urb$to <- 4
modulate_tm_selva <- summarize_selva %>% filter(expander==1)
modulate_tm_selva$to <- 9


modulate_tm <- rbind(modulate_tm_agri, modulate_tm_urb, modulate_tm_selva)

modulate_tm$Percent <- modulate_tm$sum_area/modulate_tm$area_cat

modulate_tm <- modulate_tm %>% select(from,to,Percent) 
modulate_tm <- modulate_tm %>% filter(from != 4)
modulate_tm <- modulate_tm %>% filter(from != 6)
modulate_tm <- modulate_tm %>% arrange(from)

names(modulate_tm)[names(modulate_tm) == "from"] <- "From*"
names(modulate_tm)[names(modulate_tm) == "to"] <- "To*"

file <- "C:/Dropbox (LANCIS)/cambio_cobertura_ca/dinamica_runs/corrida_x/modulate_tm.csv"

write.csv(modulate_tm, file, row.names = FALSE)

summarize_agri$to <- 2
summarize_agri$to_str <- "Agropecuario"

summarize_urb$to <- 4
summarize_urb$to_str <- "Urbano"

summarize_selva$to <- 9
summarize_selva$to_str <- "Selva"

patch_stats <- rbind(summarize_agri, summarize_urb, summarize_selva)

patch_stats$expander <- patch_stats$expander %>% replace_na(0)   
patch_stats_expander <- patch_stats %>% filter(expander == 1)
patch_stats_patcher <- patch_stats %>% filter(expander == 0)

patch_stats_patcher <- patch_stats_patcher %>% filter(from != 6)
patch_stats_patcher <- patch_stats_patcher %>% filter(from != 4)
patch_stats_expander <- patch_stats_expander %>% filter(from != 6)
patch_stats_expander <- patch_stats_expander %>% filter(from != 4)

patch_stats_expander$transition <- paste0("from_",patch_stats_expander$from,"_to_",patch_stats_expander$to)
patch_stats_patcher$transition <- paste0("from_",patch_stats_patcher$from,"_to_",patch_stats_patcher$to)

#From*	 To*	 Mean_Patch_Size	 Patch_Size_Variance	 Patch_Isometry

#expander
patch_stats_expander <- patch_stats_expander %>% select(from,to,mean_area_year, var_area_year)

names(patch_stats_expander)[names(patch_stats_expander) == "from"] <- "From*"
names(patch_stats_expander)[names(patch_stats_expander) == "to"] <- "To*"
names(patch_stats_expander)[names(patch_stats_expander) == "mean_area_year"] <- "Mean_Patch_Size"
names(patch_stats_expander)[names(patch_stats_expander) == "var_area_year"] <- "Patch_Size_Variance"


patch_stats_expander$Patch_Isometry <- 1

file <- "C:/Dropbox (LANCIS)/cambio_cobertura_ca/dinamica_runs/corrida_x/expander_parameters.csv"

write.csv(patch_stats_expander, file, row.names = FALSE)

# patcher
patch_stats_patcher <- patch_stats_patcher %>% select(from,to,mean_area_year, var_area_year)

names(patch_stats_patcher)[names(patch_stats_patcher) == "from"] <- "From*"
names(patch_stats_patcher)[names(patch_stats_patcher) == "to"] <- "To*"
names(patch_stats_patcher)[names(patch_stats_patcher) == "mean_area_year"] <- "Mean_Patch_Size"
names(patch_stats_patcher)[names(patch_stats_patcher) == "var_area_year"] <- "Patch_Size_Variance"


patch_stats_patcher$Patch_Isometry <- 1

file <- "C:/Dropbox (LANCIS)/cambio_cobertura_ca/dinamica_runs/corrida_x/patcher_parameters.csv"

write.csv(patch_stats_patcher, file, row.names = FALSE)




# id	Clase_v4
# 1	Acuícola
# 2	Agricultura
# 4	Asentamiento humano
# 6	Cuerpo de agua
# 7	Manglar, petén, tular e hidrófila
# 9	Selva
# 11	Sin vegetación
# 14	Duna costera
# 17	ND


