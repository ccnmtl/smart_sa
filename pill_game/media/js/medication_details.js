/*
(11:48:56 AM) Jessica Rowe: we shouldn't use the term 'group'
(11:57:10 AM) Jessica Rowe: and we need to not say 'group: blah blah'
(11:49:02 AM) Jessica Rowe: just gray boxes would be fine
    //OKL


(11:58:18 AM) Jessica Rowe: one more thing
(11:58:30 AM) Jessica Rowe: we can't display the 'every 12 hrs' thing
    OK DONE


(11:48:08 AM) Jessica Rowe: i just sent you the final pill image
(11:48:45 AM) Jessica Rowe: aluvia and kaletra are the same drug
    OK DONE
(11:56:03 AM) Jessica Rowe: they just need to be positioned in the same box
(11:52:49 AM) Jessica Rowe: as far as I can tell from research on kaletra  the mg amount is 133/33 mg 


(11:52:49 AM) Jessica Rowe: as far as I can tell from research on kaletra  the mg amount is 133/33 mg 
(11:56:27 AM) Jessica Rowe: and I would like to put dosage info on kaletra
(11:56:31 AM) Jessica Rowe: but I can't  find it
(11:56:39 AM) eddie: ok i'll just say n/a


*/



arv_pill_types = [
    //// L I N E     O N E  :
    //STAVUDINE / d4T:
    {
        smart_id : 'stavudine30'
        ,line: '1'
        ,group:'Stavir / d4T'
        ,brand:'Stavir / d4T'
        ,pill_label:'Stavir'
        ,marketed_by:'Aspen'
        ,dose_mg:'30'
        ,abbrev:'d4T'
        ,every_x_hrs:'12'
        ,how:''
        ,when:''
        ,food:''
        ,image:'stavudine30mg_aspen.png'
    }
    ,{
        smart_id : 'generic_d4t'
        ,line: '1'
        ,group:'Stavir / d4T'
        ,brand:'Stavir / d4T'
        ,pill_label:'Generic d4T (Sonke)'
        ,marketed_by:'sonke'
        ,dose_mg:'30'
        ,abbrev:'d4T'
        ,every_x_hrs:'12'
        ,how:''
        ,when:''
        ,food:''
        ,image:'stavudine30_alt.png'
    }
    
    
    
    // LAMIVUDINE:
    ,{
        smart_id : 'lamivudine150'
        ,line: '1'
        ,group:'Lamivudine'
        ,brand:'Lamivudine'
        ,pill_label:'Aspen Lamivudine'
        ,marketed_by:'Aspen'
        ,dose_mg:'150'
        ,abbrev:'3TC'
        ,every_x_hrs:'12'
        ,how:''
        ,when:''
        ,food:''    
        ,image:'lamivudine150_aspen.png'
    }
    ,{
        smart_id : 'lamivudine_sonke'
        ,line: '1'
        ,group:'Lamivudine'
        ,brand:'Lamivudine'
        ,pill_label:'Sonke Lamivudine'
        ,marketed_by:'Sonke'
        ,dose_mg:'150'
        ,abbrev:'3TC'
        ,every_x_hrs:'12'
        ,how:''
        ,when:''
        ,food:''
        ,image:'lamivudine_sonke.png'
    }
    
    //TENOFOVIR:
    ,{
        smart_id : 'tenofovir'
        ,line: '1'
        ,group:'Viread'
        ,brand:'Viread'
        ,pill_label:'Viread (tenofovir)'
        ,marketed_by:'Gilead Sciences'
        ,dose_mg:'300'
        ,abbrev:'?'
        ,every_x_hrs:'n/a'
        ,how:''
        ,when:''
        ,food:''
        ,image:'tenofovir_viread.png'
    }
    
    //NEVIRAPINE:
    ,{
        smart_id : 'nevirapine200'
        ,line: '1'
        ,group:'Nevirapine'
        ,brand:'Nevirapine'
        ,pill_label:'Nevirapine'
        ,marketed_by:'Aspen'
        ,dose_mg:'200'
        ,abbrev:'NVP'
        ,every_x_hrs:'12'
        ,how:''
        ,when:''
        ,food:''
        ,image:'navirapine200_aspen.png'
    }
    
    //EFAVIRENZ and STOCRIN:
    ,{
        smart_id : 'stocrin200'
        ,line: '1'
        ,group:'Efavirenz / Stocrin'
        ,brand:'Stocrin'
        ,pill_label:'Stocrin (Efavirenz)'
        ,marketed_by:'Merck'
        ,dose_mg:'200'
        ,abbrev:'EFV'
        ,every_x_hrs:'24'
        ,how:''
        ,when:'Night'
        ,food:''
        ,image:'efavirenz_stocrin200g.png'
    }
    ,{
        smart_id : 'aspen_efavirenz'
        ,line: '1'
        ,group:'Efavirenz / Stocrin'
        ,brand:'Stocrin'
        ,pill_label:'Aspen Efavirenz'
        ,marketed_by:'Aspen'
        ,dose_mg:'600'
        ,abbrev:'EFV'
        ,every_x_hrs:'24'
        ,how:''
        ,when:'Night'
        ,food:''
        ,image:'aspen_evavirenz_600mg.png'
    }
    ,{
        smart_id : 'adco_efavirenz'
        ,line: '1'
        ,group:'Efavirenz / Stocrin'
        ,brand:'Efavirenz'
        ,pill_label:'Adco Efavirenz'
        ,marketed_by:'adco'
        ,dose_mg:'600'
        ,abbrev:'EFV'
        ,every_x_hrs:'24'
        ,how:''
        ,when:'Night'
        ,food:''
        ,image:'efavirenz_alt600.png'
    }
    
    
    
    //// L I N E     T W O  :
    
    //LOPINAVIR / RITONAVIR:
    ,{
        smart_id : 'aluvia_200'
        ,line: '2'
        ,group:'Lopinavir / Ritonavir'
        ,brand:'Aluvia'
        ,pill_label:'Aluvia (lopinavir/ritonavir)'
        ,marketed_by:'Abbott'
        ,dose_mg:'200/50'
        ,abbrev:'LPV/R'
        ,every_x_hrs:'12'
        ,how:''
        ,when:''
        ,food:'With food'
        ,image:'aluvia2.png'
    }
    ,{
        smart_id : 'kaletra'
        ,line: '2'
        ,group:'Lopinavir / Ritonavir'
        ,brand:'Kaletra'
        ,pill_label:'Kaletra'
        ,marketed_by:'Abbott'
        ,dose_mg:'133/33'
        ,abbrev:'LPV/R'
        ,every_x_hrs:'12'
        ,how:''
        ,when:''
        ,food:'With food'
        ,image:'kaletra.png'
    }
    
    //DIDANOSINE:
    
    ,{
        smart_id : 'aspen_didanosine100'
        ,line: '2'
        ,group:'Didanosine'
        ,brand:'Didanosine'
        ,marketed_by:'Aspen'
        ,pill_label:'Aspen Didanosine'
        ,dose_mg:'100'
        ,abbrev:'ddl'
        ,every_x_hrs:'24'
        ,how:'dissolve pill in water'
        ,when:'Half-hour before breakfast'
        ,food:'Empty Stomach'
        ,image:'didanosine100_aspen.png'
    }
    ,{
        smart_id : 'sonke_didanosine100'
        ,line: '2'
        ,group:'Didanosine'
        ,brand:'Didanosine'
        ,pill_label:'Sonke Didanosine'
        ,marketed_by:'Sonke'
        ,dose_mg:'100'
        ,abbrev:'ddl'
        ,every_x_hrs:'24'
        ,how:'dissolve pill in water'
        ,when:'Half-hour before breakfast'
        ,food:'Empty Stomach'
        ,image:'didanosine100_aspen.png' // NOTE: REUSING THE PICTURE FOR ASPEN DIDANOSINE
    }
    ,{
        smart_id : 'aspen_didanosine_50'
        ,line: '2'
        ,group:'Didanosine'
        ,brand:'Didanosine'
        ,pill_label:'Aspen Didanosine'
        ,marketed_by:'Aspen'
        ,dose_mg:'50'
        ,abbrev:'ddl'
        ,every_x_hrs:'24'
        ,how:'dissolve pill in water'
        ,when:'Half-hour before breakfast'
        ,food:'Empty Stomach'
        ,image:'didanosine50_aspen.png'
    }
    ,{
        smart_id : 'sonke_didanosine_50'
        ,line: '2'
        ,group:'Didanosine'
        ,brand:'Didanosine'
        ,pill_label:'Sonke Didanosine'
        ,marketed_by:'Sonke'
        ,dose_mg:'50'
        ,abbrev:'ddl'
        ,every_x_hrs:'24'
        ,how:'dissolve pill in water'
        ,when:'Half-hour before breakfast'
        ,food:'Empty Stomach'
        ,image:'didanosine_sonke_50.png'
    }
    //ZIDOVUDINE:
    ,{
        smart_id : 'zidovudine300'
        ,line: '2'
        ,group:'Zidovudine'
        ,brand:'Zidovudine'
        ,pill_label:'Zidovudine'
        ,marketed_by:'Aspen'
        ,dose_mg:'300'
        ,abbrev:'AZT'
        ,every_x_hrs:'12'
        ,how:''
        ,when:''
        ,food:''
        ,image:'zivoduvine300.png'
    }
]

