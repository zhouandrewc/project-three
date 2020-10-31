
**************************************************************************
   Label           : 2001 Family Wealth Data
   Rows            : 7406
   Columns         : 38
   ASCII File Date : March 2, 2011
*************************************************************************.

FILE HANDLE PSID / NAME = '[PATH]\WLTH2001.TXT' LRECL = 130 .
DATA LIST FILE = PSID FIXED /
      S500            1 - 1         S501            2 - 6         S502            7 - 7    
      S502A           8 - 8         S503            9 - 17        S503A          18 - 18   
      S504           19 - 19        S504A          20 - 20        S505           21 - 29   
      S505A          30 - 30        S506           31 - 31        S506A          32 - 32   
      S507           33 - 41        S507A          42 - 42        S508           43 - 43   
      S508A          44 - 44        S509           45 - 53        S509A          54 - 54   
      S510           55 - 55        S510A          56 - 56        S511           57 - 65   
      S511A          66 - 66        S513           67 - 75        S513A          76 - 76   
      S514           77 - 77        S514A          78 - 78        S515           79 - 87   
      S515A          88 - 88        S518           89 - 89        S518A          90 - 90   
      S519           91 - 99        S519A         100 - 100       S520          101 - 109  
      S520A         110 - 110       S516          111 - 119       S516A         120 - 120  
      S517          121 - 129       S517A         130 - 130  
   .
   EXECUTE .
   VARIABLE LABELS 
      S500       "2001 WEALTH FILE RELEASE NUMBER"                 
      S501       "2001 FAMILY ID"                                  
      S502       "IMP WTR FARM/BUS (W10) 01"                       
      S502A      "ACC WTR FARM/BUS (W10) 01"                       
      S503       "IMP VALUE FARM/BUS (W11) 01"                     
      S503A      "ACC VALUE FARM/BUS (W11) 01"                     
      S504       "IMP WTR CHECKING/SAVING (W27) 01"                
      S504A      "ACC WTR CHECKING/SAVING (W27) 01"                
      S505       "IMP VAL CHECKING/SAVING (W28) 01"                
      S505A      "ACC VAL CHECKING/SAVING (W28) 01"                
      S506       "IMP WTR OTH DEBT (W38) 01"                       
      S506A      "ACC WTR OTH DEBT (W38) 01"                       
      S507       "IMP VALUE OTH DEBT (W39) 01"                     
      S507A      "ACC VALUE OTH DEBT (W39) 01"                     
      S508       "IMP WTR OTH REAL ESTATE (W1) 01"                 
      S508A      "ACC WTR OTH REAL ESTATE (W1) 01"                 
      S509       "IMP VAL OTH REAL ESTATE (W2) 01"                 
      S509A      "ACC VAL OTH REAL ESTATE (W2) 01"                 
      S510       "IMP WTR STOCKS (W15) 01"                         
      S510A      "ACC WTR STOCKS (W15) 01"                         
      S511       "IMP VALUE STOCKS (W16) 01"                       
      S511A      "ACC VALUE STOCKS (W16) 01"                       
      S513       "IMP VALUE VEHICLES (W6) 01"                      
      S513A      "ACC VALUE VEHICLES (W6) 01"                      
      S514       "IMP WTR OTH ASSETS (W33) 01"                     
      S514A      "ACC WTR OTH ASSETS (W33) 01"                     
      S515       "IMP VALUE OTH ASSETS (W34) 01"                   
      S515A      "ACC VALUE OTH ASSETS (W34) 01"                   
      S518       "IMP WTR ANNUITY/IRA (W21) 01"                    
      S518A      "ACC WTR ANNUITY/IRA (W21) 01"                    
      S519       "IMP VALUE ANNUITY/IRA (W22) 01"                  
      S519A      "ACC VALUE ANNUITY/IRA (W22) 01"                  
      S520       "IMP VALUE HOME EQUITY 01"                        
      S520A      "ACC VALUE HOME EQUITY 01"                        
      S516       "IMP WEALTH W/O EQUITY (WEALTH1) 01"              
      S516A      "ACC WEALTH W/O EQUITY (WEALTH1) 01"              
      S517       "IMP WEALTH W/ EQUITY (WEALTH2) 01"               
      S517A      "ACC WEALTH W/ EQUITY (WEALTH2) 01"               
   .
