/*import data: panel_0112.xlsx*/

/*gen city*/
gen city = 0
replace city = 1 if (place_id == 1) | (place_id == 5)
replace city = . if (place_id == 27)


/*model 1*/
eststo: reg growth policy i.ym if (place_id != 27) & (month > 2) & (month < 7), r 

eststo: reg num policy i.ym if (place_id != 27) & (month > 2) & (month < 7), r 

esttab
estimates clear

/*----------------------switch model------------------------*/

/*model 2*/
xtset place_id ym

eststo: xtreg growth policy if (place_id != 27) & (month > 2) & (month < 7), fe r
/*entity effect*/

eststo: xtreg num policy if (place_id != 27) & (month > 2) & (month < 7), fe r
/*entity effect*/

eststo: xtreg growth policy i.ym if (place_id != 27) & (month > 2) & (month < 7), fe r

eststo: xtreg num policy i.ym if (place_id != 27) & (month > 2) & (month < 7), fe r

esttab
estimates clear

/*----------------------switch model------------------------*/

/*DID*/
/*top2*/
eststo: quietly xtreg growth policy##city i.ym if (place_id != 27) & (month > 2) & (month < 7), fe r

eststo: quietly xtreg num policy##city i.ym if (place_id != 27) & (month > 2) & (month < 7), fe r

/////////switch interaction term////////
/*top5*/
replace city = 1 if (city_size >= 22) & (city_size != 27)

eststo: quietly xtreg growth policy##city i.ym if (place_id != 27) & (month > 2) & (month < 7), fe r

eststo: quietly xtreg num policy##city i.ym if (place_id != 27) & (month > 2) & (month < 7), fe r

/////////switch interaction term////////
/*order of city size, city_size -> larger size, larger order*/
eststo: quietly xtreg growth policy##c.city_size i.ym if (place_id != 27) & (month > 2) & (month < 7), fe r

eststo: quietly xtreg num policy##c.city_size i.ym if (place_id != 27) & (month > 2) & (month < 7), fe r

esttab
estimates clear

/*----------------------other try------------------------*/
reg growth city i.year i.month if (place_id != 27) & (month > 2) & (month < 7), r
/*-.014002, 0.479: 城市的遷入成長率相對非城市也減少*/

/////////switch interaction term////////
eststo: quietly xtreg growth policy##c.total_num i.year i.month if (place_id != 27) & (month > 2) & (month < 7), fe r
/*coef = 2.95e-07, p = 0.111*/

eststo: quietly xtreg num policy##c.total_num i.year i.month if (place_id != 27) & (month > 2) & (month < 7), fe r
/*coef = -.0006489, p = 0.000*/