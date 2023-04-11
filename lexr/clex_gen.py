def f4(self): #START
    self.tokWs=Ws._0
    return f5 #WS
def f5(self): #WS
    self.srcCh0=ch=self.srcA[self.src+0]
    g_logc.ch(self, 0, ch)
    return Lut5.get(ch, f36) #WS+1
def f7(self): #WS.Spa
    self.tokWs|=Ws.H
    return f8 #WS.Spa+1
def f8(self): #WS.Spa+1
    self.src+=1
    return f5 #WS
def f19(self): #WS.Nl
    self.tokWs|=Ws.Eol
    return f20 #WS.Nl+1
def f20(self): #WS.Nl+1
    self.src+=1
    return f21 #WS.Nl+2
def f21(self): #WS.Nl+2
    self.lineInc(0)
    return f5 #WS
def f22(self): #WS.Cr
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut22.get(ch, f19) #WS.Nl
def f24(self): #WS.Cr.Nl
    self.tokWs|=Ws.Eol
    return f25 #WS.Cr.Nl+1
def f25(self): #WS.Cr.Nl+1
    self.src+=2
    return f21 #WS.Nl+2
def f31(self): #WS.x00
    self.tokSrc=self.src
    return f32 #WS.x00+1
def f32(self): #WS.x00+1
    self.tokWs|=Ws.Eol
    self.tokWs|=Ws.Eof
    return f33 #WS.x00+2
def f33(self): #WS.x00+2
    self.tokTyp=TokTyp.Eof
    return f34 #WS.x00+3
def f34(self): #WS.x00+3
    self.tokAdd()
    return f35 #WS.x00+4
def f35(self): #WS.x00+4
    raise TermStopException()
    return f2 #<Term>
def f36(self): #WS+1
    self.tokSrc=self.src
    return f37 #WS+2
def f37(self): #WS+2
    self.acc(self.srcCh0)
    return f38 #WS+3
def f38(self): #WS+3
    self.accTyp=AccTyp._0
    return f39 #WS+4
def f39(self): #WS+4
    self.tokTyp=TokTyp.Other
    return f40 #QUOT_FIN
def f40(self): #QUOT_FIN
    self.tokAddAcc()
    return f41 #QUOT_FIN+1
def f41(self): #QUOT_FIN+1
    self.src+=1
    return f4 #START
def f42(self): #WS.Sla+1
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut42.get(ch, f158) #PUNC_Sla
def f44(self): #WS.Sla+1.Sta
    self.src+=2
    return f45 #SLST
def f45(self): #SLST
    ch=self.srcA[self.src+0]
    g_logc.ch(self, 0, ch)
    return Lut45.get(ch, f53) #SLST.Sta+1
def f47(self): #WS.Sla+1.Sla
    self.src+=2
    return f48 #SLSL
def f48(self): #SLSL
    ch=self.srcA[self.src+0]
    g_logc.ch(self, 0, ch)
    return Lut48.get(ch, f76) #SLSL+1
def f49(self): #SLST.Sta
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut49.get(ch, f53) #SLST.Sta+1
def f51(self): #SLST.Sta.Sla
    self.tokWs|=Ws.H
    return f52 #SLST.Sta.Sla+1
def f52(self): #SLST.Sta.Sla+1
    self.src+=2
    return f5 #WS
def f53(self): #SLST.Sta+1
    self.src+=1
    return f45 #SLST
def f55(self): #SLST.Nl
    self.src+=1
    return f56 #SLST.Nl+1
def f56(self): #SLST.Nl+1
    self.lineInc(0)
    return f45 #SLST
def f57(self): #SLST.Cr
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut57.get(ch, f55) #SLST.Nl
def f59(self): #SLST.Cr.Nl
    self.src+=2
    return f56 #SLST.Nl+1
def f76(self): #SLSL+1
    self.src+=1
    return f48 #SLSL
def f79(self): #PUNC_Sbl
    self.tokTyp=TokTyp.Sbl
    return f80 #PUNC_Sbl+1
def f80(self): #PUNC_Sbl+1
    self.tokAdd()
    return f8 #WS.Spa+1
def f84(self): #PUNC_Sbr
    self.tokTyp=TokTyp.Sbr
    return f80 #PUNC_Sbl+1
def f89(self): #PUNC_Pl
    self.tokTyp=TokTyp.Pl
    return f80 #PUNC_Sbl+1
def f94(self): #PUNC_Pr
    self.tokTyp=TokTyp.Pr
    return f80 #PUNC_Sbl+1
def f99(self): #PUNC_Cbl
    self.tokTyp=TokTyp.Cbl
    return f80 #PUNC_Sbl+1
def f104(self): #PUNC_Cbr
    self.tokTyp=TokTyp.Cbr
    return f80 #PUNC_Sbl+1
def f107(self): #WS.Dot+1
    self.srcCh0=ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut107.get(ch, f109) #PUNC_Dot
def f109(self): #PUNC_Dot
    self.tokTyp=TokTyp.Dot
    return f80 #PUNC_Sbl+1
def f112(self): #WS.Min+1
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut112.get(ch, f144) #PUNC_Min
def f115(self): #PUNC_Min_Gt
    self.tokTyp=TokTyp.Min_Gt
    return f116 #PUNC_Min_Gt+1
def f116(self): #PUNC_Min_Gt+1
    self.tokAdd()
    return f52 #SLST.Sta.Sla+1
def f118(self): #WS.Plu+1
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut118.get(ch, f140) #PUNC_Plu
def f121(self): #PUNC_Plu_Plu
    self.tokTyp=TokTyp.Plu_Plu
    return f116 #PUNC_Min_Gt+1
def f126(self): #PUNC_Min_Min
    self.tokTyp=TokTyp.Min_Min
    return f116 #PUNC_Min_Gt+1
def f129(self): #WS.Amp+1
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut129.get(ch, f131) #PUNC_Amp
def f131(self): #PUNC_Amp
    self.tokTyp=TokTyp.Amp
    return f80 #PUNC_Sbl+1
def f134(self): #WS.Sta+1
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut134.get(ch, f136) #PUNC_Sta
def f136(self): #PUNC_Sta
    self.tokTyp=TokTyp.Sta
    return f80 #PUNC_Sbl+1
def f140(self): #PUNC_Plu
    self.tokTyp=TokTyp.Plu
    return f80 #PUNC_Sbl+1
def f144(self): #PUNC_Min
    self.tokTyp=TokTyp.Min
    return f80 #PUNC_Sbl+1
def f149(self): #PUNC_Til
    self.tokTyp=TokTyp.Til
    return f80 #PUNC_Sbl+1
def f152(self): #WS.Exc+1
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut152.get(ch, f154) #PUNC_Exc
def f154(self): #PUNC_Exc
    self.tokTyp=TokTyp.Exc
    return f80 #PUNC_Sbl+1
def f158(self): #PUNC_Sla
    self.tokTyp=TokTyp.Sla
    return f80 #PUNC_Sbl+1
def f161(self): #WS.Per+1
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut161.get(ch, f163) #PUNC_Per
def f163(self): #PUNC_Per
    self.tokTyp=TokTyp.Per
    return f80 #PUNC_Sbl+1
def f166(self): #WS.Lt+1
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut166.get(ch, f179) #PUNC_Lt
def f167(self): #WS.Lt+1.Lt
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut167.get(ch, f169) #PUNC_Lt_Lt
def f169(self): #PUNC_Lt_Lt
    self.tokTyp=TokTyp.Lt_Lt
    return f116 #PUNC_Min_Gt+1
def f172(self): #WS.Gt+1
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut172.get(ch, f183) #PUNC_Gt
def f173(self): #WS.Gt+1.Gt
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut173.get(ch, f175) #PUNC_Gt_Gt
def f175(self): #PUNC_Gt_Gt
    self.tokTyp=TokTyp.Gt_Gt
    return f116 #PUNC_Min_Gt+1
def f179(self): #PUNC_Lt
    self.tokTyp=TokTyp.Lt
    return f80 #PUNC_Sbl+1
def f183(self): #PUNC_Gt
    self.tokTyp=TokTyp.Gt
    return f80 #PUNC_Sbl+1
def f188(self): #PUNC_Lt_Equ
    self.tokTyp=TokTyp.Lt_Equ
    return f116 #PUNC_Min_Gt+1
def f193(self): #PUNC_Gt_Equ
    self.tokTyp=TokTyp.Gt_Equ
    return f116 #PUNC_Min_Gt+1
def f196(self): #WS.Equ+1
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut196.get(ch, f249) #PUNC_Equ
def f199(self): #PUNC_Equ_Equ
    self.tokTyp=TokTyp.Equ_Equ
    return f116 #PUNC_Min_Gt+1
def f204(self): #PUNC_Exc_Equ
    self.tokTyp=TokTyp.Exc_Equ
    return f116 #PUNC_Min_Gt+1
def f207(self): #WS.Car+1
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut207.get(ch, f209) #PUNC_Car
def f209(self): #PUNC_Car
    self.tokTyp=TokTyp.Car
    return f80 #PUNC_Sbl+1
def f212(self): #WS.Bar+1
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut212.get(ch, f214) #PUNC_Bar
def f214(self): #PUNC_Bar
    self.tokTyp=TokTyp.Bar
    return f80 #PUNC_Sbl+1
def f219(self): #PUNC_Amp_Amp
    self.tokTyp=TokTyp.Amp_Amp
    return f116 #PUNC_Min_Gt+1
def f224(self): #PUNC_Bar_Bar
    self.tokTyp=TokTyp.Bar_Bar
    return f116 #PUNC_Min_Gt+1
def f229(self): #PUNC_Qm
    self.tokTyp=TokTyp.Qm
    return f80 #PUNC_Sbl+1
def f232(self): #WS.Col+1
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut232.get(ch, f234) #PUNC_Col
def f234(self): #PUNC_Col
    self.tokTyp=TokTyp.Col
    return f80 #PUNC_Sbl+1
def f239(self): #PUNC_Sem
    self.tokTyp=TokTyp.Sem
    return f80 #PUNC_Sbl+1
def f242(self): #WS.Dot+1.Dot+1
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut242.get(ch, f349) #PUNC_Dot_Dot
def f245(self): #PUNC_Dot_Dot_Dot
    self.tokTyp=TokTyp.Dot_Dot_Dot
    return f246 #PUNC_Dot_Dot_Dot+1
def f246(self): #PUNC_Dot_Dot_Dot+1
    self.tokAdd()
    return f247 #PUNC_Dot_Dot_Dot+2
def f247(self): #PUNC_Dot_Dot_Dot+2
    self.src+=3
    return f5 #WS
def f249(self): #PUNC_Equ
    self.tokTyp=TokTyp.Equ
    return f80 #PUNC_Sbl+1
def f254(self): #PUNC_Sta_Equ
    self.tokTyp=TokTyp.Sta_Equ
    return f116 #PUNC_Min_Gt+1
def f259(self): #PUNC_Sla_Equ
    self.tokTyp=TokTyp.Sla_Equ
    return f116 #PUNC_Min_Gt+1
def f264(self): #PUNC_Per_Equ
    self.tokTyp=TokTyp.Per_Equ
    return f116 #PUNC_Min_Gt+1
def f269(self): #PUNC_Plu_Equ
    self.tokTyp=TokTyp.Plu_Equ
    return f116 #PUNC_Min_Gt+1
def f274(self): #PUNC_Min_Equ
    self.tokTyp=TokTyp.Min_Equ
    return f116 #PUNC_Min_Gt+1
def f279(self): #PUNC_Lt_Lt_Equ
    self.tokTyp=TokTyp.Lt_Lt_Equ
    return f246 #PUNC_Dot_Dot_Dot+1
def f284(self): #PUNC_Gt_Gt_Equ
    self.tokTyp=TokTyp.Gt_Gt_Equ
    return f246 #PUNC_Dot_Dot_Dot+1
def f289(self): #PUNC_Amp_Equ
    self.tokTyp=TokTyp.Amp_Equ
    return f116 #PUNC_Min_Gt+1
def f294(self): #PUNC_Car_Equ
    self.tokTyp=TokTyp.Car_Equ
    return f116 #PUNC_Min_Gt+1
def f299(self): #PUNC_Bar_Equ
    self.tokTyp=TokTyp.Bar_Equ
    return f116 #PUNC_Min_Gt+1
def f304(self): #PUNC_Com
    self.tokTyp=TokTyp.Com
    return f80 #PUNC_Sbl+1
def f307(self): #WS.Has+1
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut307.get(ch, f309) #PUNC_Has
def f309(self): #PUNC_Has
    self.tokTyp=TokTyp.Has
    return f80 #PUNC_Sbl+1
def f314(self): #PUNC_Has_Has
    self.tokTyp=TokTyp.Has_Has
    return f116 #PUNC_Min_Gt+1
def f319(self): #PUNC_Lt_Col
    self.tokTyp=TokTyp.Lt_Col
    return f116 #PUNC_Min_Gt+1
def f324(self): #PUNC_Col_Gt
    self.tokTyp=TokTyp.Col_Gt
    return f116 #PUNC_Min_Gt+1
def f329(self): #PUNC_Lt_Per
    self.tokTyp=TokTyp.Lt_Per
    return f116 #PUNC_Min_Gt+1
def f334(self): #PUNC_Per_Gt
    self.tokTyp=TokTyp.Per_Gt
    return f116 #PUNC_Min_Gt+1
def f337(self): #WS.Per+1.Col
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut337.get(ch, f339) #PUNC_Per_Col
def f339(self): #PUNC_Per_Col
    self.tokTyp=TokTyp.Per_Col
    return f116 #PUNC_Min_Gt+1
def f342(self): #WS.Per+1.Col.Per+1
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut342.get(ch, f354) #PUNC_Per_Col_Per
def f345(self): #PUNC_Per_Col_Per_Col
    self.tokTyp=TokTyp.Per_Col_Per_Col
    return f346 #PUNC_Per_Col_Per_Col+1
def f346(self): #PUNC_Per_Col_Per_Col+1
    self.tokAdd()
    return f347 #PUNC_Per_Col_Per_Col+2
def f347(self): #PUNC_Per_Col_Per_Col+2
    self.src+=4
    return f5 #WS
def f349(self): #PUNC_Dot_Dot
    self.tokTyp=TokTyp.Dot
    return f350 #PUNC_Dot_Dot+1
def f350(self): #PUNC_Dot_Dot+1
    self.tokAdd()
    return f351 #PUNC_Dot_Dot+2
def f351(self): #PUNC_Dot_Dot+2
    self.src+=1
    return f352 #PUNC_Dot_Dot+3
def f352(self): #PUNC_Dot_Dot+3
    self.tokSrc=self.srcTmp0+1
    return f107 #WS.Dot+1
def f354(self): #PUNC_Per_Col_Per
    self.tokTyp=TokTyp.Per_Col
    return f355 #PUNC_Per_Col_Per+1
def f355(self): #PUNC_Per_Col_Per+1
    self.tokAdd()
    return f356 #PUNC_Per_Col_Per+2
def f356(self): #PUNC_Per_Col_Per+2
    self.src+=2
    return f357 #PUNC_Per_Col_Per+3
def f357(self): #PUNC_Per_Col_Per+3
    self.tokSrc=self.srcTmp0+2
    return f161 #WS.Per+1
def f359(self): #WS.0+1
    self.acc(self.srcCh0)
    return f360 #WS.0+2
def f360(self): #WS.0+2
    self.src+=1
    return f361 #PPN_1
def f361(self): #PPN_1
    self.srcCh0=ch=self.srcA[self.src+0]
    g_logc.ch(self, 0, ch)
    return Lut361.get(ch, f1607) #PPN_FIN
def f390(self): #WS.Dot+1.0
    self.acc('.')
    return f391 #WS.Dot+1.0+1
def f391(self): #WS.Dot+1.0+1
    self.acc(self.srcCh0)
    return f392 #WS.Dot+1.0+2
def f392(self): #WS.Dot+1.0+2
    self.src+=2
    return f361 #PPN_1
def f1003(self): #PPN_1.e
    self.acc(self.srcCh0)
    return f1004 #PPN_1.e+1
def f1004(self): #PPN_1.e+1
    self.src+=1
    return f1005 #PPN_EP
def f1005(self): #PPN_EP
    self.srcCh0=ch=self.srcA[self.src+0]
    g_logc.ch(self, 0, ch)
    return Lut1005.get(ch, f1607) #PPN_FIN
def f1607(self): #PPN_FIN
    self.accTyp=AccTyp._0
    return f1608 #PPN_FIN+1
def f1608(self): #PPN_FIN+1
    self.tokTyp=TokTyp.Ppn
    return f1609 #PPN_FIN+2
def f1609(self): #PPN_FIN+2
    self.tokAddAcc()
    return f4 #START
def f1611(self): #WS.A+1
    self.acc(self.srcCh0)
    return f1612 #WS.A+2
def f1612(self): #WS.A+2
    self.src+=1
    return f1613 #IDEN
def f1613(self): #IDEN
    self.srcCh0=ch=self.srcA[self.src+0]
    g_logc.ch(self, 0, ch)
    return Lut1613.get(ch, f2749) #IDEN_FIN
def f1644(self): #WS.L+1
    self.srcCh1=ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut1644.get(ch, f1611) #WS.A+1
def f1671(self): #WS.U+1
    self.srcCh1=ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut1671.get(ch, f1611) #WS.A+1
def f1749(self): #WS.u+1
    self.srcCh1=ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut1749.get(ch, f1611) #WS.A+1
def f2163(self): #WS.Bsl+1
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut2163.get(ch, f2752) #IDEN_BS_0
def f2747(self): #IDEN.Bsl
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut2747.get(ch, f2752) #IDEN_BS_0
def f2749(self): #IDEN_FIN
    self.accTyp=AccTyp._0
    return f2750 #IDEN_FIN+1
def f2750(self): #IDEN_FIN+1
    self.tokTyp=TokTyp.Iden
    return f1609 #PPN_FIN+2
def f2752(self): #IDEN_BS_0
    self.srcTmp0=self.src
    return f2753 #IDEN_BS
def f2753(self): #IDEN_BS
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut2753.get(ch, f2764) #IDEN_BS_ERR
def f2755(self): #IDEN_BS.u
    self.bsuI=4
    return f2756 #IDEN_BS.u+1
def f2756(self): #IDEN_BS.u+1
    self.tmpU=0
    return f2757 #IDEN_BS.u+2
def f2757(self): #IDEN_BS.u+2
    self.src+=2
    return f2758 #IDEN_BSU
def f2758(self): #IDEN_BSU
    self.srcCh0=ch=self.srcA[self.src+0]
    g_logc.ch(self, 0, ch)
    return Lut2758.get(ch, f2764) #IDEN_BS_ERR
def f2760(self): #IDEN_BS.U
    self.bsuI=8
    return f2756 #IDEN_BS.u+1
def f2764(self): #IDEN_BS_ERR
    self.errText(self.srcTmp0,self.src,TokErr.BsEscapeInvalid)
    return f2765 #IDEN_BS_ERR+1
def f2765(self): #IDEN_BS_ERR+1
    self.src=self.srcTmp0
    self.linePopGt()
    return f2766 #IDEN_BS_ERR+2
def f2766(self): #IDEN_BS_ERR+2
    self.acc('\\')
    return f1612 #WS.A+2
def f2769(self): #IDEN_BSU.0
    self.tmpV=ord('0')
    return f2813 #IDEN_BSU_NEXT
def f2790(self): #IDEN_BSU.A
    self.tmpV=ord('A')
    return f2813 #IDEN_BSU_NEXT
def f2802(self): #IDEN_BSU.a
    self.tmpV=ord('a')
    return f2813 #IDEN_BSU_NEXT
def f2813(self): #IDEN_BSU_NEXT
    self.tmpU*=16
    return f2814 #IDEN_BSU_NEXT+1
def f2814(self): #IDEN_BSU_NEXT+1
    self.tmpU+=ord(self.srcCh0)
    return f2815 #IDEN_BSU_NEXT+2
def f2815(self): #IDEN_BSU_NEXT+2
    self.tmpU-=self.tmpV
    return f2816 #IDEN_BSU_NEXT+3
def f2816(self): #IDEN_BSU_NEXT+3
    self.src+=1
    return f2817 #IDEN_BSU_NEXT+4
def f2817(self): #IDEN_BSU_NEXT+4
    self.bsuI-=1
    return f2818 #IDEN_BSU_NEXT+5
def f2818(self): #IDEN_BSU_NEXT+5
    
    if 0==self.bsuI:
        return f2821 #IDEN_BSU_FIN
    return f2758 #IDEN_BSU
def f2821(self): #IDEN_BSU_FIN
    self.acc(chr(self.tmpU))
    return f1613 #IDEN
def f2823(self): #WS.Dq+1
    self.accTyp=AccTyp._0
    return f2824 #WS.Dq+2
def f2824(self): #WS.Dq+2
    self.tokTyp=TokTyp.Sl
    return f2825 #WS.Dq+3
def f2825(self): #WS.Dq+3
    self.quoteCh=self.srcCh0
    return f2826 #WS.Dq+4
def f2826(self): #WS.Dq+4
    self.src+=1
    return f2827 #QUOT
def f2827(self): #QUOT
    self.srcCh0=ch=self.srcA[self.src+0]
    g_logc.ch(self, 0, ch)
    return Lut2827.get(ch, f2882) #QUOT_ACC
def f2828(self): #WS.u+1.8
    self.srcCh0=ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut2828.get(ch, f2869) #WS.u+1.8+1
def f2830(self): #WS.u+1.8.Dq
    self.accTyp=AccTyp.u8
    return f2831 #WS.u+1.8.Dq+1
def f2831(self): #WS.u+1.8.Dq+1
    self.tokTyp=TokTyp.Sl
    return f2832 #WS.u+1.8.Dq+2
def f2832(self): #WS.u+1.8.Dq+2
    self.quoteCh=self.srcCh0
    return f2833 #WS.u+1.8.Dq+3
def f2833(self): #WS.u+1.8.Dq+3
    self.src+=3
    return f2827 #QUOT
def f2835(self): #WS.u+1.Dq
    self.accTyp=AccTyp.u
    return f2836 #WS.u+1.Dq+1
def f2836(self): #WS.u+1.Dq+1
    self.tokTyp=TokTyp.Sl
    return f2837 #WS.u+1.Dq+2
def f2837(self): #WS.u+1.Dq+2
    self.quoteCh=self.srcCh1
    return f2838 #WS.u+1.Dq+3
def f2838(self): #WS.u+1.Dq+3
    self.src+=2
    return f2827 #QUOT
def f2840(self): #WS.U+1.Dq
    self.accTyp=AccTyp.U
    return f2836 #WS.u+1.Dq+1
def f2845(self): #WS.L+1.Dq
    self.accTyp=AccTyp.L
    return f2836 #WS.u+1.Dq+1
def f2850(self): #WS.Sq+1
    self.accTyp=AccTyp._0
    return f2851 #WS.Sq+2
def f2851(self): #WS.Sq+2
    self.tokTyp=TokTyp.Cc
    return f2825 #WS.Dq+3
def f2855(self): #WS.L+1.Sq
    self.accTyp=AccTyp.L
    return f2856 #WS.L+1.Sq+1
def f2856(self): #WS.L+1.Sq+1
    self.tokTyp=TokTyp.Cc
    return f2837 #WS.u+1.Dq+2
def f2860(self): #WS.u+1.Sq
    self.accTyp=AccTyp.u
    return f2856 #WS.L+1.Sq+1
def f2865(self): #WS.U+1.Sq
    self.accTyp=AccTyp.U
    return f2856 #WS.L+1.Sq+1
def f2869(self): #WS.u+1.8+1
    self.acc('u8')
    return f2870 #WS.u+1.8+2
def f2870(self): #WS.u+1.8+2
    self.src+=2
    return f1613 #IDEN
def f2872(self): #QUOT.Sq
    
    if self.quoteCh==self.srcCh0:
        return f40 #QUOT_FIN
    return f2882 #QUOT_ACC
def f2879(self): #QUOT.Bsl
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut2879.get(ch, f2880) #QUOT.Bsl+1
def f2880(self): #QUOT.Bsl+1
    self.srcTmp0=self.src
    return f2881 #QUOT_BS
def f2881(self): #QUOT_BS
    self.srcCh0=ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut2881.get(ch, f3151) #QUOT_BS_ERR
def f2882(self): #QUOT_ACC
    self.acc(self.srcCh0)
    return f2826 #WS.Dq+4
def f2887(self): #QUOT.Nl
    self.errPos(self.src,TokErr.QuotEol)
    return f2888 #QUOT.Nl+1
def f2888(self): #QUOT.Nl+1
    self.acc('\n')
    return f2889 #QUOT.Nl+2
def f2889(self): #QUOT.Nl+2
    self.src+=1
    return f2890 #QUOT.Nl+3
def f2890(self): #QUOT.Nl+3
    self.lineInc(0)
    return f2827 #QUOT
def f2891(self): #QUOT.Cr
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut2891.get(ch, f2897) #QUOT.Cr+1
def f2893(self): #QUOT.Cr.Nl
    self.errPos(self.src,TokErr.QuotEol)
    return f2894 #QUOT.Cr.Nl+1
def f2894(self): #QUOT.Cr.Nl+1
    self.acc('\r\n')
    return f2895 #QUOT.Cr.Nl+2
def f2895(self): #QUOT.Cr.Nl+2
    self.src+=2
    return f2890 #QUOT.Nl+3
def f2897(self): #QUOT.Cr+1
    self.errPos(self.src,TokErr.QuotEol)
    return f2898 #QUOT.Cr+2
def f2898(self): #QUOT.Cr+2
    self.acc('\r')
    return f2889 #QUOT.Nl+2
def f2902(self): #QUOT.x00
    self.errPos(self.src,TokErr.QuotEof)
    return f1609 #PPN_FIN+2
def f2905(self): #QUOT_BS.Dq
    self.acc(self.srcCh0)
    return f2838 #WS.u+1.Dq+3
def f2913(self): #QUOT_BS.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut2913.get(ch, f2905) #QUOT_BS.Dq
def f2917(self): #QUOT_BS.a
    self.acc('\x07')
    return f2838 #WS.u+1.Dq+3
def f2920(self): #QUOT_BS.b
    self.acc('\x08')
    return f2838 #WS.u+1.Dq+3
def f2923(self): #QUOT_BS.t
    self.acc('\t')
    return f2838 #WS.u+1.Dq+3
def f2926(self): #QUOT_BS.n
    self.acc('\n')
    return f2838 #WS.u+1.Dq+3
def f2929(self): #QUOT_BS.v
    self.acc('\x0b')
    return f2838 #WS.u+1.Dq+3
def f2932(self): #QUOT_BS.f
    self.acc('\x0c')
    return f2838 #WS.u+1.Dq+3
def f2935(self): #QUOT_BS.r
    self.acc('\r')
    return f2838 #WS.u+1.Dq+3
def f2938(self): #QUOT_BS.0
    self.tmpU=ord(self.srcCh0)
    return f2939 #QUOT_BS.0+1
def f2939(self): #QUOT_BS.0+1
    self.tmpU-=ord('0')
    return f2940 #QUOT_BS.0+2
def f2940(self): #QUOT_BS.0+2
    self.src+=2
    return f2941 #QUOT_BSO1
def f2941(self): #QUOT_BSO1
    self.srcCh0=ch=self.srcA[self.src+0]
    g_logc.ch(self, 0, ch)
    return Lut2941.get(ch, f3011) #QUOT_BSU_FIN
def f2971(self): #QUOT_BSO1.0
    self.tmpU*=8
    return f2972 #QUOT_BSO1.0+1
def f2972(self): #QUOT_BSO1.0+1
    self.tmpU+=ord(self.srcCh0)
    return f2973 #QUOT_BSO1.0+2
def f2973(self): #QUOT_BSO1.0+2
    self.tmpU-=ord('0')
    return f2974 #QUOT_BSO1.0+3
def f2974(self): #QUOT_BSO1.0+3
    self.src+=1
    return f2975 #QUOT_BSO2
def f2975(self): #QUOT_BSO2
    self.srcCh0=ch=self.srcA[self.src+0]
    g_logc.ch(self, 0, ch)
    return Lut2975.get(ch, f3011) #QUOT_BSU_FIN
def f3011(self): #QUOT_BSU_FIN
    self.acc(chr(self.tmpU))
    return f2827 #QUOT
def f3013(self): #QUOT_BSO2.0
    self.tmpU*=8
    return f3014 #QUOT_BSO2.0+1
def f3014(self): #QUOT_BSO2.0+1
    self.tmpU+=ord(self.srcCh0)
    return f3015 #QUOT_BSO2.0+2
def f3015(self): #QUOT_BSO2.0+2
    self.tmpU-=ord('0')
    return f3016 #QUOT_BSO2.0+3
def f3016(self): #QUOT_BSO2.0+3
    self.src+=1
    return f3011 #QUOT_BSU_FIN
def f3061(self): #QUOT_BS.x
    self.srcCh0=ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3061.get(ch, f3151) #QUOT_BS_ERR
def f3063(self): #QUOT_BS.x.0
    self.tmpU=ord(self.srcCh0)
    return f3064 #QUOT_BS.x.0+1
def f3064(self): #QUOT_BS.x.0+1
    self.tmpU-=ord('0')
    return f3065 #QUOT_BS.x.0+2
def f3065(self): #QUOT_BS.x.0+2
    self.src+=3
    return f3066 #QUOT_BSX
def f3066(self): #QUOT_BSX
    self.srcCh0=ch=self.srcA[self.src+0]
    g_logc.ch(self, 0, ch)
    return Lut3066.get(ch, f3011) #QUOT_BSU_FIN
def f3104(self): #QUOT_BS.x.A
    self.tmpU=ord(self.srcCh0)
    return f3105 #QUOT_BS.x.A+1
def f3105(self): #QUOT_BS.x.A+1
    self.tmpU-=ord('A')
    return f3065 #QUOT_BS.x.0+2
def f3128(self): #QUOT_BS.x.a
    self.tmpU=ord(self.srcCh0)
    return f3129 #QUOT_BS.x.a+1
def f3129(self): #QUOT_BS.x.a+1
    self.tmpU-=ord('a')
    return f3065 #QUOT_BS.x.0+2
def f3151(self): #QUOT_BS_ERR
    self.errText(self.srcTmp0,self.src,TokErr.BsEscapeInvalid)
    return f3152 #QUOT_BS_ERR+1
def f3152(self): #QUOT_BS_ERR+1
    self.src=self.srcTmp0
    self.linePopGt()
    return f3153 #QUOT_BS_ERR+2
def f3153(self): #QUOT_BS_ERR+2
    self.acc('\\')
    return f2826 #WS.Dq+4
def f3156(self): #QUOT_BSX.0
    self.tmpV=ord('0')
    return f3201 #QUOT_BSX_NEXT
def f3177(self): #QUOT_BSX.A
    self.tmpV=ord('A')
    return f3201 #QUOT_BSX_NEXT
def f3189(self): #QUOT_BSX.a
    self.tmpV=ord('a')
    return f3201 #QUOT_BSX_NEXT
def f3201(self): #QUOT_BSX_NEXT
    self.tmpU*=16
    return f3202 #QUOT_BSX_NEXT+1
def f3202(self): #QUOT_BSX_NEXT+1
    self.tmpU+=ord(self.srcCh0)
    return f3203 #QUOT_BSX_NEXT+2
def f3203(self): #QUOT_BSX_NEXT+2
    self.tmpU-=self.tmpV
    return f3204 #QUOT_BSX_NEXT+3
def f3204(self): #QUOT_BSX_NEXT+3
    self.src+=1
    return f3066 #QUOT_BSX
def f3206(self): #QUOT_BS.u
    self.bsuI=4
    return f3207 #QUOT_BS.u+1
def f3207(self): #QUOT_BS.u+1
    self.tmpU=0
    return f3208 #QUOT_BS.u+2
def f3208(self): #QUOT_BS.u+2
    self.src+=2
    return f3209 #QUOT_BSU
def f3209(self): #QUOT_BSU
    self.srcCh0=ch=self.srcA[self.src+0]
    g_logc.ch(self, 0, ch)
    return Lut3209.get(ch, f3151) #QUOT_BS_ERR
def f3211(self): #QUOT_BS.U
    self.bsuI=8
    return f3207 #QUOT_BS.u+1
def f3220(self): #QUOT_BSU.0
    self.tmpV=ord('0')
    return f3264 #QUOT_BSU_NEXT
def f3241(self): #QUOT_BSU.A
    self.tmpV=ord('A')
    return f3264 #QUOT_BSU_NEXT
def f3253(self): #QUOT_BSU.a
    self.tmpV=ord('a')
    return f3264 #QUOT_BSU_NEXT
def f3264(self): #QUOT_BSU_NEXT
    self.tmpU*=16
    return f3265 #QUOT_BSU_NEXT+1
def f3265(self): #QUOT_BSU_NEXT+1
    self.tmpU+=ord(self.srcCh0)
    return f3266 #QUOT_BSU_NEXT+2
def f3266(self): #QUOT_BSU_NEXT+2
    self.tmpU-=self.tmpV
    return f3267 #QUOT_BSU_NEXT+3
def f3267(self): #QUOT_BSU_NEXT+3
    self.src+=1
    return f3268 #QUOT_BSU_NEXT+4
def f3268(self): #QUOT_BSU_NEXT+4
    self.bsuI-=1
    return f3269 #QUOT_BSU_NEXT+5
def f3269(self): #QUOT_BSU_NEXT+5
    
    if 0==self.bsuI:
        return f3011 #QUOT_BSU_FIN
    return f3209 #QUOT_BSU
def f3276(self): #WS.Bsl+1.Cr
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3276.get(ch, f25) #WS.Cr.Nl+1
def f3278(self): #WS.Bsl+1.Cr.Nl
    self.src+=3
    return f21 #WS.Nl+2
def f3282(self): #WS.Sla+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3282.get(ch, f158) #PUNC_Sla
def f3284(self): #WS.Sla+1.Bsl.Nl
    self.src+=2
    return f3285 #WS.Sla+1.Bsl.Nl+1
def f3285(self): #WS.Sla+1.Bsl.Nl+1
    self.lineInc(1)
    return f42 #WS.Sla+1
def f3286(self): #WS.Sla+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3286.get(ch, f3284) #WS.Sla+1.Bsl.Nl
def f3288(self): #WS.Sla+1.Bsl.Cr.Nl
    self.src+=3
    return f3285 #WS.Sla+1.Bsl.Nl+1
def f3292(self): #SLST.Bsl
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut3292.get(ch, f53) #SLST.Sta+1
def f3296(self): #SLST.Bsl.Cr
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3296.get(ch, f59) #SLST.Cr.Nl
def f3298(self): #SLST.Bsl.Cr.Nl
    self.src+=3
    return f56 #SLST.Nl+1
def f3302(self): #SLSL.Bsl
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut3302.get(ch, f76) #SLSL+1
def f3304(self): #SLSL.Bsl.Nl
    self.src+=2
    return f3305 #SLSL.Bsl.Nl+1
def f3305(self): #SLSL.Bsl.Nl+1
    self.lineInc(0)
    return f48 #SLSL
def f3306(self): #SLSL.Bsl.Cr
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3306.get(ch, f3304) #SLSL.Bsl.Nl
def f3308(self): #SLSL.Bsl.Cr.Nl
    self.src+=3
    return f3305 #SLSL.Bsl.Nl+1
def f3312(self): #SLST.Sta.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3312.get(ch, f53) #SLST.Sta+1
def f3314(self): #SLST.Sta.Bsl.Nl
    self.src+=2
    return f3315 #SLST.Sta.Bsl.Nl+1
def f3315(self): #SLST.Sta.Bsl.Nl+1
    self.lineInc(1)
    return f49 #SLST.Sta
def f3316(self): #SLST.Sta.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3316.get(ch, f3314) #SLST.Sta.Bsl.Nl
def f3318(self): #SLST.Sta.Bsl.Cr.Nl
    self.src+=3
    return f3315 #SLST.Sta.Bsl.Nl+1
def f3322(self): #WS.Dot+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3322.get(ch, f109) #PUNC_Dot
def f3324(self): #WS.Dot+1.Bsl.Nl
    self.src+=2
    return f3325 #WS.Dot+1.Bsl.Nl+1
def f3325(self): #WS.Dot+1.Bsl.Nl+1
    self.lineInc(1)
    return f107 #WS.Dot+1
def f3326(self): #WS.Dot+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3326.get(ch, f3324) #WS.Dot+1.Bsl.Nl
def f3328(self): #WS.Dot+1.Bsl.Cr.Nl
    self.src+=3
    return f3325 #WS.Dot+1.Bsl.Nl+1
def f3332(self): #WS.Min+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3332.get(ch, f144) #PUNC_Min
def f3334(self): #WS.Min+1.Bsl.Nl
    self.src+=2
    return f3335 #WS.Min+1.Bsl.Nl+1
def f3335(self): #WS.Min+1.Bsl.Nl+1
    self.lineInc(1)
    return f112 #WS.Min+1
def f3336(self): #WS.Min+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3336.get(ch, f3334) #WS.Min+1.Bsl.Nl
def f3338(self): #WS.Min+1.Bsl.Cr.Nl
    self.src+=3
    return f3335 #WS.Min+1.Bsl.Nl+1
def f3342(self): #WS.Plu+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3342.get(ch, f140) #PUNC_Plu
def f3344(self): #WS.Plu+1.Bsl.Nl
    self.src+=2
    return f3345 #WS.Plu+1.Bsl.Nl+1
def f3345(self): #WS.Plu+1.Bsl.Nl+1
    self.lineInc(1)
    return f118 #WS.Plu+1
def f3346(self): #WS.Plu+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3346.get(ch, f3344) #WS.Plu+1.Bsl.Nl
def f3348(self): #WS.Plu+1.Bsl.Cr.Nl
    self.src+=3
    return f3345 #WS.Plu+1.Bsl.Nl+1
def f3352(self): #WS.Amp+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3352.get(ch, f131) #PUNC_Amp
def f3354(self): #WS.Amp+1.Bsl.Nl
    self.src+=2
    return f3355 #WS.Amp+1.Bsl.Nl+1
def f3355(self): #WS.Amp+1.Bsl.Nl+1
    self.lineInc(1)
    return f129 #WS.Amp+1
def f3356(self): #WS.Amp+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3356.get(ch, f3354) #WS.Amp+1.Bsl.Nl
def f3358(self): #WS.Amp+1.Bsl.Cr.Nl
    self.src+=3
    return f3355 #WS.Amp+1.Bsl.Nl+1
def f3362(self): #WS.Sta+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3362.get(ch, f136) #PUNC_Sta
def f3364(self): #WS.Sta+1.Bsl.Nl
    self.src+=2
    return f3365 #WS.Sta+1.Bsl.Nl+1
def f3365(self): #WS.Sta+1.Bsl.Nl+1
    self.lineInc(1)
    return f134 #WS.Sta+1
def f3366(self): #WS.Sta+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3366.get(ch, f3364) #WS.Sta+1.Bsl.Nl
def f3368(self): #WS.Sta+1.Bsl.Cr.Nl
    self.src+=3
    return f3365 #WS.Sta+1.Bsl.Nl+1
def f3372(self): #WS.Exc+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3372.get(ch, f154) #PUNC_Exc
def f3374(self): #WS.Exc+1.Bsl.Nl
    self.src+=2
    return f3375 #WS.Exc+1.Bsl.Nl+1
def f3375(self): #WS.Exc+1.Bsl.Nl+1
    self.lineInc(1)
    return f152 #WS.Exc+1
def f3376(self): #WS.Exc+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3376.get(ch, f3374) #WS.Exc+1.Bsl.Nl
def f3378(self): #WS.Exc+1.Bsl.Cr.Nl
    self.src+=3
    return f3375 #WS.Exc+1.Bsl.Nl+1
def f3382(self): #WS.Per+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3382.get(ch, f163) #PUNC_Per
def f3384(self): #WS.Per+1.Bsl.Nl
    self.src+=2
    return f3385 #WS.Per+1.Bsl.Nl+1
def f3385(self): #WS.Per+1.Bsl.Nl+1
    self.lineInc(1)
    return f161 #WS.Per+1
def f3386(self): #WS.Per+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3386.get(ch, f3384) #WS.Per+1.Bsl.Nl
def f3388(self): #WS.Per+1.Bsl.Cr.Nl
    self.src+=3
    return f3385 #WS.Per+1.Bsl.Nl+1
def f3392(self): #WS.Lt+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3392.get(ch, f179) #PUNC_Lt
def f3394(self): #WS.Lt+1.Bsl.Nl
    self.src+=2
    return f3395 #WS.Lt+1.Bsl.Nl+1
def f3395(self): #WS.Lt+1.Bsl.Nl+1
    self.lineInc(1)
    return f166 #WS.Lt+1
def f3396(self): #WS.Lt+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3396.get(ch, f3394) #WS.Lt+1.Bsl.Nl
def f3398(self): #WS.Lt+1.Bsl.Cr.Nl
    self.src+=3
    return f3395 #WS.Lt+1.Bsl.Nl+1
def f3402(self): #WS.Lt+1.Lt.Bsl
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3402.get(ch, f169) #PUNC_Lt_Lt
def f3404(self): #WS.Lt+1.Lt.Bsl.Nl
    self.src+=2
    return f3405 #WS.Lt+1.Lt.Bsl.Nl+1
def f3405(self): #WS.Lt+1.Lt.Bsl.Nl+1
    self.lineInc(2)
    return f167 #WS.Lt+1.Lt
def f3406(self): #WS.Lt+1.Lt.Bsl.Cr
    ch=self.srcA[self.src+4]
    g_logc.ch(self, 4, ch)
    return Lut3406.get(ch, f3404) #WS.Lt+1.Lt.Bsl.Nl
def f3408(self): #WS.Lt+1.Lt.Bsl.Cr.Nl
    self.src+=3
    return f3405 #WS.Lt+1.Lt.Bsl.Nl+1
def f3412(self): #WS.Gt+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3412.get(ch, f183) #PUNC_Gt
def f3414(self): #WS.Gt+1.Bsl.Nl
    self.src+=2
    return f3415 #WS.Gt+1.Bsl.Nl+1
def f3415(self): #WS.Gt+1.Bsl.Nl+1
    self.lineInc(1)
    return f172 #WS.Gt+1
def f3416(self): #WS.Gt+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3416.get(ch, f3414) #WS.Gt+1.Bsl.Nl
def f3418(self): #WS.Gt+1.Bsl.Cr.Nl
    self.src+=3
    return f3415 #WS.Gt+1.Bsl.Nl+1
def f3422(self): #WS.Gt+1.Gt.Bsl
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3422.get(ch, f175) #PUNC_Gt_Gt
def f3424(self): #WS.Gt+1.Gt.Bsl.Nl
    self.src+=2
    return f3425 #WS.Gt+1.Gt.Bsl.Nl+1
def f3425(self): #WS.Gt+1.Gt.Bsl.Nl+1
    self.lineInc(2)
    return f173 #WS.Gt+1.Gt
def f3426(self): #WS.Gt+1.Gt.Bsl.Cr
    ch=self.srcA[self.src+4]
    g_logc.ch(self, 4, ch)
    return Lut3426.get(ch, f3424) #WS.Gt+1.Gt.Bsl.Nl
def f3428(self): #WS.Gt+1.Gt.Bsl.Cr.Nl
    self.src+=3
    return f3425 #WS.Gt+1.Gt.Bsl.Nl+1
def f3432(self): #WS.Equ+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3432.get(ch, f249) #PUNC_Equ
def f3434(self): #WS.Equ+1.Bsl.Nl
    self.src+=2
    return f3435 #WS.Equ+1.Bsl.Nl+1
def f3435(self): #WS.Equ+1.Bsl.Nl+1
    self.lineInc(1)
    return f196 #WS.Equ+1
def f3436(self): #WS.Equ+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3436.get(ch, f3434) #WS.Equ+1.Bsl.Nl
def f3438(self): #WS.Equ+1.Bsl.Cr.Nl
    self.src+=3
    return f3435 #WS.Equ+1.Bsl.Nl+1
def f3442(self): #WS.Car+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3442.get(ch, f209) #PUNC_Car
def f3444(self): #WS.Car+1.Bsl.Nl
    self.src+=2
    return f3445 #WS.Car+1.Bsl.Nl+1
def f3445(self): #WS.Car+1.Bsl.Nl+1
    self.lineInc(1)
    return f207 #WS.Car+1
def f3446(self): #WS.Car+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3446.get(ch, f3444) #WS.Car+1.Bsl.Nl
def f3448(self): #WS.Car+1.Bsl.Cr.Nl
    self.src+=3
    return f3445 #WS.Car+1.Bsl.Nl+1
def f3452(self): #WS.Bar+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3452.get(ch, f214) #PUNC_Bar
def f3454(self): #WS.Bar+1.Bsl.Nl
    self.src+=2
    return f3455 #WS.Bar+1.Bsl.Nl+1
def f3455(self): #WS.Bar+1.Bsl.Nl+1
    self.lineInc(1)
    return f212 #WS.Bar+1
def f3456(self): #WS.Bar+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3456.get(ch, f3454) #WS.Bar+1.Bsl.Nl
def f3458(self): #WS.Bar+1.Bsl.Cr.Nl
    self.src+=3
    return f3455 #WS.Bar+1.Bsl.Nl+1
def f3462(self): #WS.Col+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3462.get(ch, f234) #PUNC_Col
def f3464(self): #WS.Col+1.Bsl.Nl
    self.src+=2
    return f3465 #WS.Col+1.Bsl.Nl+1
def f3465(self): #WS.Col+1.Bsl.Nl+1
    self.lineInc(1)
    return f232 #WS.Col+1
def f3466(self): #WS.Col+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3466.get(ch, f3464) #WS.Col+1.Bsl.Nl
def f3468(self): #WS.Col+1.Bsl.Cr.Nl
    self.src+=3
    return f3465 #WS.Col+1.Bsl.Nl+1
def f3472(self): #WS.Dot+1.Dot+1.Bsl
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3472.get(ch, f349) #PUNC_Dot_Dot
def f3474(self): #WS.Dot+1.Dot+1.Bsl.Nl
    self.src+=2
    return f3475 #WS.Dot+1.Dot+1.Bsl.Nl+1
def f3475(self): #WS.Dot+1.Dot+1.Bsl.Nl+1
    self.lineInc(2)
    return f242 #WS.Dot+1.Dot+1
def f3476(self): #WS.Dot+1.Dot+1.Bsl.Cr
    ch=self.srcA[self.src+4]
    g_logc.ch(self, 4, ch)
    return Lut3476.get(ch, f3474) #WS.Dot+1.Dot+1.Bsl.Nl
def f3478(self): #WS.Dot+1.Dot+1.Bsl.Cr.Nl
    self.src+=3
    return f3475 #WS.Dot+1.Dot+1.Bsl.Nl+1
def f3482(self): #WS.Has+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3482.get(ch, f309) #PUNC_Has
def f3484(self): #WS.Has+1.Bsl.Nl
    self.src+=2
    return f3485 #WS.Has+1.Bsl.Nl+1
def f3485(self): #WS.Has+1.Bsl.Nl+1
    self.lineInc(1)
    return f307 #WS.Has+1
def f3486(self): #WS.Has+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3486.get(ch, f3484) #WS.Has+1.Bsl.Nl
def f3488(self): #WS.Has+1.Bsl.Cr.Nl
    self.src+=3
    return f3485 #WS.Has+1.Bsl.Nl+1
def f3492(self): #WS.Per+1.Col.Bsl
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3492.get(ch, f339) #PUNC_Per_Col
def f3494(self): #WS.Per+1.Col.Bsl.Nl
    self.src+=2
    return f3495 #WS.Per+1.Col.Bsl.Nl+1
def f3495(self): #WS.Per+1.Col.Bsl.Nl+1
    self.lineInc(2)
    return f337 #WS.Per+1.Col
def f3496(self): #WS.Per+1.Col.Bsl.Cr
    ch=self.srcA[self.src+4]
    g_logc.ch(self, 4, ch)
    return Lut3496.get(ch, f3494) #WS.Per+1.Col.Bsl.Nl
def f3498(self): #WS.Per+1.Col.Bsl.Cr.Nl
    self.src+=3
    return f3495 #WS.Per+1.Col.Bsl.Nl+1
def f3502(self): #WS.Per+1.Col.Per+1.Bsl
    ch=self.srcA[self.src+4]
    g_logc.ch(self, 4, ch)
    return Lut3502.get(ch, f354) #PUNC_Per_Col_Per
def f3504(self): #WS.Per+1.Col.Per+1.Bsl.Nl
    self.src+=2
    return f3505 #WS.Per+1.Col.Per+1.Bsl.Nl+1
def f3505(self): #WS.Per+1.Col.Per+1.Bsl.Nl+1
    self.lineInc(3)
    return f342 #WS.Per+1.Col.Per+1
def f3506(self): #WS.Per+1.Col.Per+1.Bsl.Cr
    ch=self.srcA[self.src+5]
    g_logc.ch(self, 5, ch)
    return Lut3506.get(ch, f3504) #WS.Per+1.Col.Per+1.Bsl.Nl
def f3508(self): #WS.Per+1.Col.Per+1.Bsl.Cr.Nl
    self.src+=3
    return f3505 #WS.Per+1.Col.Per+1.Bsl.Nl+1
def f3512(self): #PPN_1.Bsl
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut3512.get(ch, f1607) #PPN_FIN
def f3514(self): #PPN_1.Bsl.Nl
    self.src+=2
    return f3515 #PPN_1.Bsl.Nl+1
def f3515(self): #PPN_1.Bsl.Nl+1
    self.lineInc(0)
    return f361 #PPN_1
def f3516(self): #PPN_1.Bsl.Cr
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3516.get(ch, f3514) #PPN_1.Bsl.Nl
def f3518(self): #PPN_1.Bsl.Cr.Nl
    self.src+=3
    return f3515 #PPN_1.Bsl.Nl+1
def f3522(self): #PPN_EP.Bsl
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut3522.get(ch, f1607) #PPN_FIN
def f3524(self): #PPN_EP.Bsl.Nl
    self.src+=2
    return f3525 #PPN_EP.Bsl.Nl+1
def f3525(self): #PPN_EP.Bsl.Nl+1
    self.lineInc(0)
    return f1005 #PPN_EP
def f3526(self): #PPN_EP.Bsl.Cr
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3526.get(ch, f3524) #PPN_EP.Bsl.Nl
def f3528(self): #PPN_EP.Bsl.Cr.Nl
    self.src+=3
    return f3525 #PPN_EP.Bsl.Nl+1
def f3533(self): #IDEN.Bsl.Nl
    self.src+=2
    return f3534 #IDEN.Bsl.Nl+1
def f3534(self): #IDEN.Bsl.Nl+1
    self.lineInc(0)
    return f1613 #IDEN
def f3535(self): #IDEN.Bsl.Cr
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3535.get(ch, f3533) #IDEN.Bsl.Nl
def f3537(self): #IDEN.Bsl.Cr.Nl
    self.src+=3
    return f3534 #IDEN.Bsl.Nl+1
def f3541(self): #WS.L+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3541.get(ch, f1611) #WS.A+1
def f3543(self): #WS.L+1.Bsl.Nl
    self.src+=2
    return f3544 #WS.L+1.Bsl.Nl+1
def f3544(self): #WS.L+1.Bsl.Nl+1
    self.lineInc(1)
    return f1644 #WS.L+1
def f3545(self): #WS.L+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3545.get(ch, f3543) #WS.L+1.Bsl.Nl
def f3547(self): #WS.L+1.Bsl.Cr.Nl
    self.src+=3
    return f3544 #WS.L+1.Bsl.Nl+1
def f3551(self): #WS.U+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3551.get(ch, f1611) #WS.A+1
def f3553(self): #WS.U+1.Bsl.Nl
    self.src+=2
    return f3554 #WS.U+1.Bsl.Nl+1
def f3554(self): #WS.U+1.Bsl.Nl+1
    self.lineInc(1)
    return f1671 #WS.U+1
def f3555(self): #WS.U+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3555.get(ch, f3553) #WS.U+1.Bsl.Nl
def f3557(self): #WS.U+1.Bsl.Cr.Nl
    self.src+=3
    return f3554 #WS.U+1.Bsl.Nl+1
def f3561(self): #WS.u+1.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3561.get(ch, f1611) #WS.A+1
def f3563(self): #WS.u+1.Bsl.Nl
    self.src+=2
    return f3564 #WS.u+1.Bsl.Nl+1
def f3564(self): #WS.u+1.Bsl.Nl+1
    self.lineInc(1)
    return f1749 #WS.u+1
def f3565(self): #WS.u+1.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3565.get(ch, f3563) #WS.u+1.Bsl.Nl
def f3567(self): #WS.u+1.Bsl.Cr.Nl
    self.src+=3
    return f3564 #WS.u+1.Bsl.Nl+1
def f3571(self): #IDEN_BS.Bsl
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3571.get(ch, f2764) #IDEN_BS_ERR
def f3573(self): #IDEN_BS.Bsl.Nl
    self.src+=2
    return f3574 #IDEN_BS.Bsl.Nl+1
def f3574(self): #IDEN_BS.Bsl.Nl+1
    self.lineInc(1)
    return f2753 #IDEN_BS
def f3575(self): #IDEN_BS.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3575.get(ch, f3573) #IDEN_BS.Bsl.Nl
def f3577(self): #IDEN_BS.Bsl.Cr.Nl
    self.src+=3
    return f3574 #IDEN_BS.Bsl.Nl+1
def f3581(self): #IDEN_BSU.Bsl
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut3581.get(ch, f2764) #IDEN_BS_ERR
def f3583(self): #IDEN_BSU.Bsl.Nl
    self.src+=2
    return f3584 #IDEN_BSU.Bsl.Nl+1
def f3584(self): #IDEN_BSU.Bsl.Nl+1
    self.lineInc(0)
    return f2758 #IDEN_BSU
def f3585(self): #IDEN_BSU.Bsl.Cr
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3585.get(ch, f3583) #IDEN_BSU.Bsl.Nl
def f3587(self): #IDEN_BSU.Bsl.Cr.Nl
    self.src+=3
    return f3584 #IDEN_BSU.Bsl.Nl+1
def f3594(self): #QUOT.Bsl.Cr
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3594.get(ch, f2895) #QUOT.Cr.Nl+2
def f3596(self): #QUOT.Bsl.Cr.Nl
    self.src+=3
    return f2890 #QUOT.Nl+3
def f3600(self): #WS.u+1.8.Bsl
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3600.get(ch, f2869) #WS.u+1.8+1
def f3602(self): #WS.u+1.8.Bsl.Nl
    self.src+=2
    return f3603 #WS.u+1.8.Bsl.Nl+1
def f3603(self): #WS.u+1.8.Bsl.Nl+1
    self.lineInc(2)
    return f2828 #WS.u+1.8
def f3604(self): #WS.u+1.8.Bsl.Cr
    ch=self.srcA[self.src+4]
    g_logc.ch(self, 4, ch)
    return Lut3604.get(ch, f3602) #WS.u+1.8.Bsl.Nl
def f3606(self): #WS.u+1.8.Bsl.Cr.Nl
    self.src+=3
    return f3603 #WS.u+1.8.Bsl.Nl+1
def f3611(self): #QUOT_BS.Bsl.Nl
    self.src+=2
    return f3612 #QUOT_BS.Bsl.Nl+1
def f3612(self): #QUOT_BS.Bsl.Nl+1
    self.lineInc(1)
    return f2881 #QUOT_BS
def f3613(self): #QUOT_BS.Bsl.Cr
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3613.get(ch, f3611) #QUOT_BS.Bsl.Nl
def f3615(self): #QUOT_BS.Bsl.Cr.Nl
    self.src+=3
    return f3612 #QUOT_BS.Bsl.Nl+1
def f3619(self): #QUOT_BSO1.Bsl
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut3619.get(ch, f3011) #QUOT_BSU_FIN
def f3621(self): #QUOT_BSO1.Bsl.Nl
    self.src+=2
    return f3622 #QUOT_BSO1.Bsl.Nl+1
def f3622(self): #QUOT_BSO1.Bsl.Nl+1
    self.lineInc(0)
    return f2941 #QUOT_BSO1
def f3623(self): #QUOT_BSO1.Bsl.Cr
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3623.get(ch, f3621) #QUOT_BSO1.Bsl.Nl
def f3625(self): #QUOT_BSO1.Bsl.Cr.Nl
    self.src+=3
    return f3622 #QUOT_BSO1.Bsl.Nl+1
def f3629(self): #QUOT_BSO2.Bsl
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut3629.get(ch, f3011) #QUOT_BSU_FIN
def f3631(self): #QUOT_BSO2.Bsl.Nl
    self.src+=2
    return f3632 #QUOT_BSO2.Bsl.Nl+1
def f3632(self): #QUOT_BSO2.Bsl.Nl+1
    self.lineInc(0)
    return f2975 #QUOT_BSO2
def f3633(self): #QUOT_BSO2.Bsl.Cr
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3633.get(ch, f3631) #QUOT_BSO2.Bsl.Nl
def f3635(self): #QUOT_BSO2.Bsl.Cr.Nl
    self.src+=3
    return f3632 #QUOT_BSO2.Bsl.Nl+1
def f3639(self): #QUOT_BS.x.Bsl
    ch=self.srcA[self.src+3]
    g_logc.ch(self, 3, ch)
    return Lut3639.get(ch, f3151) #QUOT_BS_ERR
def f3641(self): #QUOT_BS.x.Bsl.Nl
    self.src+=2
    return f3642 #QUOT_BS.x.Bsl.Nl+1
def f3642(self): #QUOT_BS.x.Bsl.Nl+1
    self.lineInc(2)
    return f3061 #QUOT_BS.x
def f3643(self): #QUOT_BS.x.Bsl.Cr
    ch=self.srcA[self.src+4]
    g_logc.ch(self, 4, ch)
    return Lut3643.get(ch, f3641) #QUOT_BS.x.Bsl.Nl
def f3645(self): #QUOT_BS.x.Bsl.Cr.Nl
    self.src+=3
    return f3642 #QUOT_BS.x.Bsl.Nl+1
def f3649(self): #QUOT_BSX.Bsl
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut3649.get(ch, f3011) #QUOT_BSU_FIN
def f3651(self): #QUOT_BSX.Bsl.Nl
    self.src+=2
    return f3652 #QUOT_BSX.Bsl.Nl+1
def f3652(self): #QUOT_BSX.Bsl.Nl+1
    self.lineInc(0)
    return f3066 #QUOT_BSX
def f3653(self): #QUOT_BSX.Bsl.Cr
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3653.get(ch, f3651) #QUOT_BSX.Bsl.Nl
def f3655(self): #QUOT_BSX.Bsl.Cr.Nl
    self.src+=3
    return f3652 #QUOT_BSX.Bsl.Nl+1
def f3659(self): #QUOT_BSU.Bsl
    ch=self.srcA[self.src+1]
    g_logc.ch(self, 1, ch)
    return Lut3659.get(ch, f3151) #QUOT_BS_ERR
def f3661(self): #QUOT_BSU.Bsl.Nl
    self.src+=2
    return f3662 #QUOT_BSU.Bsl.Nl+1
def f3662(self): #QUOT_BSU.Bsl.Nl+1
    self.lineInc(0)
    return f3209 #QUOT_BSU
def f3663(self): #QUOT_BSU.Bsl.Cr
    ch=self.srcA[self.src+2]
    g_logc.ch(self, 2, ch)
    return Lut3663.get(ch, f3661) #QUOT_BSU.Bsl.Nl
def f3665(self): #QUOT_BSU.Bsl.Cr.Nl
    self.src+=3
    return f3662 #QUOT_BSU.Bsl.Nl+1
def f3706(self): #WS.Per+1.Col.Per
    self.srcTmp0=self.src
    return f342 #WS.Per+1.Col.Per+1
def f3708(self): #WS.Dot+1.Dot
    self.srcTmp0=self.src
    return f242 #WS.Dot+1.Dot+1
def f3710(self): #WS.Sla
    self.tokSrc=self.src
    return f42 #WS.Sla+1
def f3712(self): #WS.Sbl
    self.tokSrc=self.src
    return f79 #PUNC_Sbl
def f3714(self): #WS.Sbr
    self.tokSrc=self.src
    return f84 #PUNC_Sbr
def f3716(self): #WS.Pl
    self.tokSrc=self.src
    return f89 #PUNC_Pl
def f3718(self): #WS.Pr
    self.tokSrc=self.src
    return f94 #PUNC_Pr
def f3720(self): #WS.Cbl
    self.tokSrc=self.src
    return f99 #PUNC_Cbl
def f3722(self): #WS.Cbr
    self.tokSrc=self.src
    return f104 #PUNC_Cbr
def f3724(self): #WS.Dot
    self.tokSrc=self.src
    return f107 #WS.Dot+1
def f3726(self): #WS.Min
    self.tokSrc=self.src
    return f112 #WS.Min+1
def f3728(self): #WS.Plu
    self.tokSrc=self.src
    return f118 #WS.Plu+1
def f3730(self): #WS.Amp
    self.tokSrc=self.src
    return f129 #WS.Amp+1
def f3732(self): #WS.Sta
    self.tokSrc=self.src
    return f134 #WS.Sta+1
def f3734(self): #WS.Til
    self.tokSrc=self.src
    return f149 #PUNC_Til
def f3736(self): #WS.Exc
    self.tokSrc=self.src
    return f152 #WS.Exc+1
def f3738(self): #WS.Per
    self.tokSrc=self.src
    return f161 #WS.Per+1
def f3740(self): #WS.Lt
    self.tokSrc=self.src
    return f166 #WS.Lt+1
def f3742(self): #WS.Gt
    self.tokSrc=self.src
    return f172 #WS.Gt+1
def f3744(self): #WS.Equ
    self.tokSrc=self.src
    return f196 #WS.Equ+1
def f3746(self): #WS.Car
    self.tokSrc=self.src
    return f207 #WS.Car+1
def f3748(self): #WS.Bar
    self.tokSrc=self.src
    return f212 #WS.Bar+1
def f3750(self): #WS.Qm
    self.tokSrc=self.src
    return f229 #PUNC_Qm
def f3752(self): #WS.Col
    self.tokSrc=self.src
    return f232 #WS.Col+1
def f3754(self): #WS.Sem
    self.tokSrc=self.src
    return f239 #PUNC_Sem
def f3756(self): #WS.Com
    self.tokSrc=self.src
    return f304 #PUNC_Com
def f3758(self): #WS.Has
    self.tokSrc=self.src
    return f307 #WS.Has+1
def f3760(self): #WS.0
    self.tokSrc=self.src
    return f359 #WS.0+1
def f3780(self): #WS.A
    self.tokSrc=self.src
    return f1611 #WS.A+1
def f3802(self): #WS.L
    self.tokSrc=self.src
    return f1644 #WS.L+1
def f3820(self): #WS.U
    self.tokSrc=self.src
    return f1671 #WS.U+1
def f3872(self): #WS.u
    self.tokSrc=self.src
    return f1749 #WS.u+1
def f4148(self): #WS.Bsl
    self.tokSrc=self.src
    return f2163 #WS.Bsl+1
def f4150(self): #WS.Dq
    self.tokSrc=self.src
    return f2823 #WS.Dq+1
def f4152(self): #WS.Sq
    self.tokSrc=self.src
    return f2850 #WS.Sq+1
Lut5 = { #WS
    ' ':f7, #WS.Spa
    '\t':f7, #WS.Spa
    '\x0b':f7, #WS.Spa
    '\x0c':f7, #WS.Spa
    '\n':f19, #WS.Nl
    '\r':f22, #WS.Cr
    '\x00':f31, #WS.x00
    '/':f3710, #WS.Sla
    '[':f3712, #WS.Sbl
    ']':f3714, #WS.Sbr
    '(':f3716, #WS.Pl
    ')':f3718, #WS.Pr
    '{':f3720, #WS.Cbl
    '}':f3722, #WS.Cbr
    '.':f3724, #WS.Dot
    '-':f3726, #WS.Min
    '+':f3728, #WS.Plu
    '&':f3730, #WS.Amp
    '*':f3732, #WS.Sta
    '~':f3734, #WS.Til
    '!':f3736, #WS.Exc
    '%':f3738, #WS.Per
    '<':f3740, #WS.Lt
    '>':f3742, #WS.Gt
    '=':f3744, #WS.Equ
    '^':f3746, #WS.Car
    '|':f3748, #WS.Bar
    '?':f3750, #WS.Qm
    ':':f3752, #WS.Col
    ';':f3754, #WS.Sem
    ',':f3756, #WS.Com
    '#':f3758, #WS.Has
    '0':f3760, #WS.0
    '1':f3760, #WS.0
    '2':f3760, #WS.0
    '3':f3760, #WS.0
    '4':f3760, #WS.0
    '5':f3760, #WS.0
    '6':f3760, #WS.0
    '7':f3760, #WS.0
    '8':f3760, #WS.0
    '9':f3760, #WS.0
    'A':f3780, #WS.A
    'B':f3780, #WS.A
    'C':f3780, #WS.A
    'D':f3780, #WS.A
    'E':f3780, #WS.A
    'F':f3780, #WS.A
    'G':f3780, #WS.A
    'H':f3780, #WS.A
    'I':f3780, #WS.A
    'J':f3780, #WS.A
    'K':f3780, #WS.A
    'L':f3802, #WS.L
    'M':f3780, #WS.A
    'N':f3780, #WS.A
    'O':f3780, #WS.A
    'P':f3780, #WS.A
    'Q':f3780, #WS.A
    'R':f3780, #WS.A
    'S':f3780, #WS.A
    'T':f3780, #WS.A
    'U':f3820, #WS.U
    'V':f3780, #WS.A
    'W':f3780, #WS.A
    'X':f3780, #WS.A
    'Y':f3780, #WS.A
    'Z':f3780, #WS.A
    'a':f3780, #WS.A
    'b':f3780, #WS.A
    'c':f3780, #WS.A
    'd':f3780, #WS.A
    'e':f3780, #WS.A
    'f':f3780, #WS.A
    'g':f3780, #WS.A
    'h':f3780, #WS.A
    'i':f3780, #WS.A
    'j':f3780, #WS.A
    'k':f3780, #WS.A
    'l':f3780, #WS.A
    'm':f3780, #WS.A
    'n':f3780, #WS.A
    'o':f3780, #WS.A
    'p':f3780, #WS.A
    'q':f3780, #WS.A
    'r':f3780, #WS.A
    's':f3780, #WS.A
    't':f3780, #WS.A
    'u':f3872, #WS.u
    'v':f3780, #WS.A
    'w':f3780, #WS.A
    'x':f3780, #WS.A
    'y':f3780, #WS.A
    'z':f3780, #WS.A
    '_':f3780, #WS.A
    '@':f3780, #WS.A
    '$':f3780, #WS.A
    '`':f3780, #WS.A
    '\x80':f3780, #WS.A
    '\x81':f3780, #WS.A
    '\x82':f3780, #WS.A
    '\x83':f3780, #WS.A
    '\x84':f3780, #WS.A
    '\x85':f3780, #WS.A
    '\x86':f3780, #WS.A
    '\x87':f3780, #WS.A
    '\x88':f3780, #WS.A
    '\x89':f3780, #WS.A
    '\x8a':f3780, #WS.A
    '\x8b':f3780, #WS.A
    '\x8c':f3780, #WS.A
    '\x8d':f3780, #WS.A
    '\x8e':f3780, #WS.A
    '\x8f':f3780, #WS.A
    '\x90':f3780, #WS.A
    '\x91':f3780, #WS.A
    '\x92':f3780, #WS.A
    '\x93':f3780, #WS.A
    '\x94':f3780, #WS.A
    '\x95':f3780, #WS.A
    '\x96':f3780, #WS.A
    '\x97':f3780, #WS.A
    '\x98':f3780, #WS.A
    '\x99':f3780, #WS.A
    '\x9a':f3780, #WS.A
    '\x9b':f3780, #WS.A
    '\x9c':f3780, #WS.A
    '\x9d':f3780, #WS.A
    '\x9e':f3780, #WS.A
    '\x9f':f3780, #WS.A
    '\xa0':f3780, #WS.A
    '¡':f3780, #WS.A
    '¢':f3780, #WS.A
    '£':f3780, #WS.A
    '¤':f3780, #WS.A
    '¥':f3780, #WS.A
    '¦':f3780, #WS.A
    '§':f3780, #WS.A
    '¨':f3780, #WS.A
    '©':f3780, #WS.A
    'ª':f3780, #WS.A
    '«':f3780, #WS.A
    '¬':f3780, #WS.A
    '\xad':f3780, #WS.A
    '®':f3780, #WS.A
    '¯':f3780, #WS.A
    '°':f3780, #WS.A
    '±':f3780, #WS.A
    '²':f3780, #WS.A
    '³':f3780, #WS.A
    '´':f3780, #WS.A
    'µ':f3780, #WS.A
    '¶':f3780, #WS.A
    '·':f3780, #WS.A
    '¸':f3780, #WS.A
    '¹':f3780, #WS.A
    'º':f3780, #WS.A
    '»':f3780, #WS.A
    '¼':f3780, #WS.A
    '½':f3780, #WS.A
    '¾':f3780, #WS.A
    '¿':f3780, #WS.A
    'À':f3780, #WS.A
    'Á':f3780, #WS.A
    'Â':f3780, #WS.A
    'Ã':f3780, #WS.A
    'Ä':f3780, #WS.A
    'Å':f3780, #WS.A
    'Æ':f3780, #WS.A
    'Ç':f3780, #WS.A
    'È':f3780, #WS.A
    'É':f3780, #WS.A
    'Ê':f3780, #WS.A
    'Ë':f3780, #WS.A
    'Ì':f3780, #WS.A
    'Í':f3780, #WS.A
    'Î':f3780, #WS.A
    'Ï':f3780, #WS.A
    'Ð':f3780, #WS.A
    'Ñ':f3780, #WS.A
    'Ò':f3780, #WS.A
    'Ó':f3780, #WS.A
    'Ô':f3780, #WS.A
    'Õ':f3780, #WS.A
    'Ö':f3780, #WS.A
    '×':f3780, #WS.A
    'Ø':f3780, #WS.A
    'Ù':f3780, #WS.A
    'Ú':f3780, #WS.A
    'Û':f3780, #WS.A
    'Ü':f3780, #WS.A
    'Ý':f3780, #WS.A
    'Þ':f3780, #WS.A
    'ß':f3780, #WS.A
    'à':f3780, #WS.A
    'á':f3780, #WS.A
    'â':f3780, #WS.A
    'ã':f3780, #WS.A
    'ä':f3780, #WS.A
    'å':f3780, #WS.A
    'æ':f3780, #WS.A
    'ç':f3780, #WS.A
    'è':f3780, #WS.A
    'é':f3780, #WS.A
    'ê':f3780, #WS.A
    'ë':f3780, #WS.A
    'ì':f3780, #WS.A
    'í':f3780, #WS.A
    'î':f3780, #WS.A
    'ï':f3780, #WS.A
    'ð':f3780, #WS.A
    'ñ':f3780, #WS.A
    'ò':f3780, #WS.A
    'ó':f3780, #WS.A
    'ô':f3780, #WS.A
    'õ':f3780, #WS.A
    'ö':f3780, #WS.A
    '÷':f3780, #WS.A
    'ø':f3780, #WS.A
    'ù':f3780, #WS.A
    'ú':f3780, #WS.A
    'û':f3780, #WS.A
    'ü':f3780, #WS.A
    'ý':f3780, #WS.A
    'þ':f3780, #WS.A
    'ÿ':f3780, #WS.A
    '\\':f4148, #WS.Bsl
    '"':f4150, #WS.Dq
    "'":f4152, #WS.Sq
}
Lut22 = { #WS.Cr
    '\n':f24, #WS.Cr.Nl
}
Lut42 = { #WS.Sla+1
    '*':f44, #WS.Sla+1.Sta
    '/':f47, #WS.Sla+1.Sla
    '=':f259, #PUNC_Sla_Equ
    '\\':f3282, #WS.Sla+1.Bsl
}
Lut45 = { #SLST
    '*':f49, #SLST.Sta
    '\n':f55, #SLST.Nl
    '\r':f57, #SLST.Cr
    '\\':f3292, #SLST.Bsl
}
Lut48 = { #SLSL
    '\n':f19, #WS.Nl
    '\r':f22, #WS.Cr
    '\\':f3302, #SLSL.Bsl
}
Lut49 = { #SLST.Sta
    '/':f51, #SLST.Sta.Sla
    '\\':f3312, #SLST.Sta.Bsl
}
Lut57 = { #SLST.Cr
    '\n':f59, #SLST.Cr.Nl
}
Lut107 = { #WS.Dot+1
    '.':f3708, #WS.Dot+1.Dot
    '0':f390, #WS.Dot+1.0
    '1':f390, #WS.Dot+1.0
    '2':f390, #WS.Dot+1.0
    '3':f390, #WS.Dot+1.0
    '4':f390, #WS.Dot+1.0
    '5':f390, #WS.Dot+1.0
    '6':f390, #WS.Dot+1.0
    '7':f390, #WS.Dot+1.0
    '8':f390, #WS.Dot+1.0
    '9':f390, #WS.Dot+1.0
    '\\':f3322, #WS.Dot+1.Bsl
}
Lut112 = { #WS.Min+1
    '>':f115, #PUNC_Min_Gt
    '-':f126, #PUNC_Min_Min
    '=':f274, #PUNC_Min_Equ
    '\\':f3332, #WS.Min+1.Bsl
}
Lut118 = { #WS.Plu+1
    '+':f121, #PUNC_Plu_Plu
    '=':f269, #PUNC_Plu_Equ
    '\\':f3342, #WS.Plu+1.Bsl
}
Lut129 = { #WS.Amp+1
    '&':f219, #PUNC_Amp_Amp
    '=':f289, #PUNC_Amp_Equ
    '\\':f3352, #WS.Amp+1.Bsl
}
Lut134 = { #WS.Sta+1
    '=':f254, #PUNC_Sta_Equ
    '\\':f3362, #WS.Sta+1.Bsl
}
Lut152 = { #WS.Exc+1
    '=':f204, #PUNC_Exc_Equ
    '\\':f3372, #WS.Exc+1.Bsl
}
Lut161 = { #WS.Per+1
    '=':f264, #PUNC_Per_Equ
    '>':f334, #PUNC_Per_Gt
    ':':f337, #WS.Per+1.Col
    '\\':f3382, #WS.Per+1.Bsl
}
Lut166 = { #WS.Lt+1
    '<':f167, #WS.Lt+1.Lt
    '=':f188, #PUNC_Lt_Equ
    ':':f319, #PUNC_Lt_Col
    '%':f329, #PUNC_Lt_Per
    '\\':f3392, #WS.Lt+1.Bsl
}
Lut167 = { #WS.Lt+1.Lt
    '=':f279, #PUNC_Lt_Lt_Equ
    '\\':f3402, #WS.Lt+1.Lt.Bsl
}
Lut172 = { #WS.Gt+1
    '>':f173, #WS.Gt+1.Gt
    '=':f193, #PUNC_Gt_Equ
    '\\':f3412, #WS.Gt+1.Bsl
}
Lut173 = { #WS.Gt+1.Gt
    '=':f284, #PUNC_Gt_Gt_Equ
    '\\':f3422, #WS.Gt+1.Gt.Bsl
}
Lut196 = { #WS.Equ+1
    '=':f199, #PUNC_Equ_Equ
    '\\':f3432, #WS.Equ+1.Bsl
}
Lut207 = { #WS.Car+1
    '=':f294, #PUNC_Car_Equ
    '\\':f3442, #WS.Car+1.Bsl
}
Lut212 = { #WS.Bar+1
    '|':f224, #PUNC_Bar_Bar
    '=':f299, #PUNC_Bar_Equ
    '\\':f3452, #WS.Bar+1.Bsl
}
Lut232 = { #WS.Col+1
    '>':f324, #PUNC_Col_Gt
    '\\':f3462, #WS.Col+1.Bsl
}
Lut242 = { #WS.Dot+1.Dot+1
    '.':f245, #PUNC_Dot_Dot_Dot
    '\\':f3472, #WS.Dot+1.Dot+1.Bsl
}
Lut307 = { #WS.Has+1
    '#':f314, #PUNC_Has_Has
    '\\':f3482, #WS.Has+1.Bsl
}
Lut337 = { #WS.Per+1.Col
    '%':f3706, #WS.Per+1.Col.Per
    '\\':f3492, #WS.Per+1.Col.Bsl
}
Lut342 = { #WS.Per+1.Col.Per+1
    ':':f345, #PUNC_Per_Col_Per_Col
    '\\':f3502, #WS.Per+1.Col.Per+1.Bsl
}
Lut361 = { #PPN_1
    'A':f359, #WS.0+1
    'B':f359, #WS.0+1
    'C':f359, #WS.0+1
    'D':f359, #WS.0+1
    'F':f359, #WS.0+1
    'G':f359, #WS.0+1
    'H':f359, #WS.0+1
    'I':f359, #WS.0+1
    'J':f359, #WS.0+1
    'K':f359, #WS.0+1
    'L':f359, #WS.0+1
    'M':f359, #WS.0+1
    'N':f359, #WS.0+1
    'O':f359, #WS.0+1
    'Q':f359, #WS.0+1
    'R':f359, #WS.0+1
    'S':f359, #WS.0+1
    'T':f359, #WS.0+1
    'U':f359, #WS.0+1
    'V':f359, #WS.0+1
    'W':f359, #WS.0+1
    'X':f359, #WS.0+1
    'Y':f359, #WS.0+1
    'Z':f359, #WS.0+1
    'a':f359, #WS.0+1
    'b':f359, #WS.0+1
    'c':f359, #WS.0+1
    'd':f359, #WS.0+1
    'f':f359, #WS.0+1
    'g':f359, #WS.0+1
    'h':f359, #WS.0+1
    'i':f359, #WS.0+1
    'j':f359, #WS.0+1
    'k':f359, #WS.0+1
    'l':f359, #WS.0+1
    'm':f359, #WS.0+1
    'n':f359, #WS.0+1
    'o':f359, #WS.0+1
    'q':f359, #WS.0+1
    'r':f359, #WS.0+1
    's':f359, #WS.0+1
    't':f359, #WS.0+1
    'u':f359, #WS.0+1
    'v':f359, #WS.0+1
    'w':f359, #WS.0+1
    'x':f359, #WS.0+1
    'y':f359, #WS.0+1
    'z':f359, #WS.0+1
    '_':f359, #WS.0+1
    '0':f359, #WS.0+1
    '1':f359, #WS.0+1
    '2':f359, #WS.0+1
    '3':f359, #WS.0+1
    '4':f359, #WS.0+1
    '5':f359, #WS.0+1
    '6':f359, #WS.0+1
    '7':f359, #WS.0+1
    '8':f359, #WS.0+1
    '9':f359, #WS.0+1
    '.':f359, #WS.0+1
    '@':f359, #WS.0+1
    '$':f359, #WS.0+1
    '`':f359, #WS.0+1
    '\x80':f359, #WS.0+1
    '\x81':f359, #WS.0+1
    '\x82':f359, #WS.0+1
    '\x83':f359, #WS.0+1
    '\x84':f359, #WS.0+1
    '\x85':f359, #WS.0+1
    '\x86':f359, #WS.0+1
    '\x87':f359, #WS.0+1
    '\x88':f359, #WS.0+1
    '\x89':f359, #WS.0+1
    '\x8a':f359, #WS.0+1
    '\x8b':f359, #WS.0+1
    '\x8c':f359, #WS.0+1
    '\x8d':f359, #WS.0+1
    '\x8e':f359, #WS.0+1
    '\x8f':f359, #WS.0+1
    '\x90':f359, #WS.0+1
    '\x91':f359, #WS.0+1
    '\x92':f359, #WS.0+1
    '\x93':f359, #WS.0+1
    '\x94':f359, #WS.0+1
    '\x95':f359, #WS.0+1
    '\x96':f359, #WS.0+1
    '\x97':f359, #WS.0+1
    '\x98':f359, #WS.0+1
    '\x99':f359, #WS.0+1
    '\x9a':f359, #WS.0+1
    '\x9b':f359, #WS.0+1
    '\x9c':f359, #WS.0+1
    '\x9d':f359, #WS.0+1
    '\x9e':f359, #WS.0+1
    '\x9f':f359, #WS.0+1
    '\xa0':f359, #WS.0+1
    '¡':f359, #WS.0+1
    '¢':f359, #WS.0+1
    '£':f359, #WS.0+1
    '¤':f359, #WS.0+1
    '¥':f359, #WS.0+1
    '¦':f359, #WS.0+1
    '§':f359, #WS.0+1
    '¨':f359, #WS.0+1
    '©':f359, #WS.0+1
    'ª':f359, #WS.0+1
    '«':f359, #WS.0+1
    '¬':f359, #WS.0+1
    '\xad':f359, #WS.0+1
    '®':f359, #WS.0+1
    '¯':f359, #WS.0+1
    '°':f359, #WS.0+1
    '±':f359, #WS.0+1
    '²':f359, #WS.0+1
    '³':f359, #WS.0+1
    '´':f359, #WS.0+1
    'µ':f359, #WS.0+1
    '¶':f359, #WS.0+1
    '·':f359, #WS.0+1
    '¸':f359, #WS.0+1
    '¹':f359, #WS.0+1
    'º':f359, #WS.0+1
    '»':f359, #WS.0+1
    '¼':f359, #WS.0+1
    '½':f359, #WS.0+1
    '¾':f359, #WS.0+1
    '¿':f359, #WS.0+1
    'À':f359, #WS.0+1
    'Á':f359, #WS.0+1
    'Â':f359, #WS.0+1
    'Ã':f359, #WS.0+1
    'Ä':f359, #WS.0+1
    'Å':f359, #WS.0+1
    'Æ':f359, #WS.0+1
    'Ç':f359, #WS.0+1
    'È':f359, #WS.0+1
    'É':f359, #WS.0+1
    'Ê':f359, #WS.0+1
    'Ë':f359, #WS.0+1
    'Ì':f359, #WS.0+1
    'Í':f359, #WS.0+1
    'Î':f359, #WS.0+1
    'Ï':f359, #WS.0+1
    'Ð':f359, #WS.0+1
    'Ñ':f359, #WS.0+1
    'Ò':f359, #WS.0+1
    'Ó':f359, #WS.0+1
    'Ô':f359, #WS.0+1
    'Õ':f359, #WS.0+1
    'Ö':f359, #WS.0+1
    '×':f359, #WS.0+1
    'Ø':f359, #WS.0+1
    'Ù':f359, #WS.0+1
    'Ú':f359, #WS.0+1
    'Û':f359, #WS.0+1
    'Ü':f359, #WS.0+1
    'Ý':f359, #WS.0+1
    'Þ':f359, #WS.0+1
    'ß':f359, #WS.0+1
    'à':f359, #WS.0+1
    'á':f359, #WS.0+1
    'â':f359, #WS.0+1
    'ã':f359, #WS.0+1
    'ä':f359, #WS.0+1
    'å':f359, #WS.0+1
    'æ':f359, #WS.0+1
    'ç':f359, #WS.0+1
    'è':f359, #WS.0+1
    'é':f359, #WS.0+1
    'ê':f359, #WS.0+1
    'ë':f359, #WS.0+1
    'ì':f359, #WS.0+1
    'í':f359, #WS.0+1
    'î':f359, #WS.0+1
    'ï':f359, #WS.0+1
    'ð':f359, #WS.0+1
    'ñ':f359, #WS.0+1
    'ò':f359, #WS.0+1
    'ó':f359, #WS.0+1
    'ô':f359, #WS.0+1
    'õ':f359, #WS.0+1
    'ö':f359, #WS.0+1
    '÷':f359, #WS.0+1
    'ø':f359, #WS.0+1
    'ù':f359, #WS.0+1
    'ú':f359, #WS.0+1
    'û':f359, #WS.0+1
    'ü':f359, #WS.0+1
    'ý':f359, #WS.0+1
    'þ':f359, #WS.0+1
    'ÿ':f359, #WS.0+1
    'e':f1003, #PPN_1.e
    'E':f1003, #PPN_1.e
    'p':f1003, #PPN_1.e
    'P':f1003, #PPN_1.e
    '\\':f3512, #PPN_1.Bsl
}
Lut1005 = { #PPN_EP
    'A':f359, #WS.0+1
    'B':f359, #WS.0+1
    'C':f359, #WS.0+1
    'D':f359, #WS.0+1
    'E':f359, #WS.0+1
    'F':f359, #WS.0+1
    'G':f359, #WS.0+1
    'H':f359, #WS.0+1
    'I':f359, #WS.0+1
    'J':f359, #WS.0+1
    'K':f359, #WS.0+1
    'L':f359, #WS.0+1
    'M':f359, #WS.0+1
    'N':f359, #WS.0+1
    'O':f359, #WS.0+1
    'P':f359, #WS.0+1
    'Q':f359, #WS.0+1
    'R':f359, #WS.0+1
    'S':f359, #WS.0+1
    'T':f359, #WS.0+1
    'U':f359, #WS.0+1
    'V':f359, #WS.0+1
    'W':f359, #WS.0+1
    'X':f359, #WS.0+1
    'Y':f359, #WS.0+1
    'Z':f359, #WS.0+1
    'a':f359, #WS.0+1
    'b':f359, #WS.0+1
    'c':f359, #WS.0+1
    'd':f359, #WS.0+1
    'e':f359, #WS.0+1
    'f':f359, #WS.0+1
    'g':f359, #WS.0+1
    'h':f359, #WS.0+1
    'i':f359, #WS.0+1
    'j':f359, #WS.0+1
    'k':f359, #WS.0+1
    'l':f359, #WS.0+1
    'm':f359, #WS.0+1
    'n':f359, #WS.0+1
    'o':f359, #WS.0+1
    'p':f359, #WS.0+1
    'q':f359, #WS.0+1
    'r':f359, #WS.0+1
    's':f359, #WS.0+1
    't':f359, #WS.0+1
    'u':f359, #WS.0+1
    'v':f359, #WS.0+1
    'w':f359, #WS.0+1
    'x':f359, #WS.0+1
    'y':f359, #WS.0+1
    'z':f359, #WS.0+1
    '_':f359, #WS.0+1
    '0':f359, #WS.0+1
    '1':f359, #WS.0+1
    '2':f359, #WS.0+1
    '3':f359, #WS.0+1
    '4':f359, #WS.0+1
    '5':f359, #WS.0+1
    '6':f359, #WS.0+1
    '7':f359, #WS.0+1
    '8':f359, #WS.0+1
    '9':f359, #WS.0+1
    '.':f359, #WS.0+1
    '+':f359, #WS.0+1
    '-':f359, #WS.0+1
    '@':f359, #WS.0+1
    '$':f359, #WS.0+1
    '`':f359, #WS.0+1
    '\x80':f359, #WS.0+1
    '\x81':f359, #WS.0+1
    '\x82':f359, #WS.0+1
    '\x83':f359, #WS.0+1
    '\x84':f359, #WS.0+1
    '\x85':f359, #WS.0+1
    '\x86':f359, #WS.0+1
    '\x87':f359, #WS.0+1
    '\x88':f359, #WS.0+1
    '\x89':f359, #WS.0+1
    '\x8a':f359, #WS.0+1
    '\x8b':f359, #WS.0+1
    '\x8c':f359, #WS.0+1
    '\x8d':f359, #WS.0+1
    '\x8e':f359, #WS.0+1
    '\x8f':f359, #WS.0+1
    '\x90':f359, #WS.0+1
    '\x91':f359, #WS.0+1
    '\x92':f359, #WS.0+1
    '\x93':f359, #WS.0+1
    '\x94':f359, #WS.0+1
    '\x95':f359, #WS.0+1
    '\x96':f359, #WS.0+1
    '\x97':f359, #WS.0+1
    '\x98':f359, #WS.0+1
    '\x99':f359, #WS.0+1
    '\x9a':f359, #WS.0+1
    '\x9b':f359, #WS.0+1
    '\x9c':f359, #WS.0+1
    '\x9d':f359, #WS.0+1
    '\x9e':f359, #WS.0+1
    '\x9f':f359, #WS.0+1
    '\xa0':f359, #WS.0+1
    '¡':f359, #WS.0+1
    '¢':f359, #WS.0+1
    '£':f359, #WS.0+1
    '¤':f359, #WS.0+1
    '¥':f359, #WS.0+1
    '¦':f359, #WS.0+1
    '§':f359, #WS.0+1
    '¨':f359, #WS.0+1
    '©':f359, #WS.0+1
    'ª':f359, #WS.0+1
    '«':f359, #WS.0+1
    '¬':f359, #WS.0+1
    '\xad':f359, #WS.0+1
    '®':f359, #WS.0+1
    '¯':f359, #WS.0+1
    '°':f359, #WS.0+1
    '±':f359, #WS.0+1
    '²':f359, #WS.0+1
    '³':f359, #WS.0+1
    '´':f359, #WS.0+1
    'µ':f359, #WS.0+1
    '¶':f359, #WS.0+1
    '·':f359, #WS.0+1
    '¸':f359, #WS.0+1
    '¹':f359, #WS.0+1
    'º':f359, #WS.0+1
    '»':f359, #WS.0+1
    '¼':f359, #WS.0+1
    '½':f359, #WS.0+1
    '¾':f359, #WS.0+1
    '¿':f359, #WS.0+1
    'À':f359, #WS.0+1
    'Á':f359, #WS.0+1
    'Â':f359, #WS.0+1
    'Ã':f359, #WS.0+1
    'Ä':f359, #WS.0+1
    'Å':f359, #WS.0+1
    'Æ':f359, #WS.0+1
    'Ç':f359, #WS.0+1
    'È':f359, #WS.0+1
    'É':f359, #WS.0+1
    'Ê':f359, #WS.0+1
    'Ë':f359, #WS.0+1
    'Ì':f359, #WS.0+1
    'Í':f359, #WS.0+1
    'Î':f359, #WS.0+1
    'Ï':f359, #WS.0+1
    'Ð':f359, #WS.0+1
    'Ñ':f359, #WS.0+1
    'Ò':f359, #WS.0+1
    'Ó':f359, #WS.0+1
    'Ô':f359, #WS.0+1
    'Õ':f359, #WS.0+1
    'Ö':f359, #WS.0+1
    '×':f359, #WS.0+1
    'Ø':f359, #WS.0+1
    'Ù':f359, #WS.0+1
    'Ú':f359, #WS.0+1
    'Û':f359, #WS.0+1
    'Ü':f359, #WS.0+1
    'Ý':f359, #WS.0+1
    'Þ':f359, #WS.0+1
    'ß':f359, #WS.0+1
    'à':f359, #WS.0+1
    'á':f359, #WS.0+1
    'â':f359, #WS.0+1
    'ã':f359, #WS.0+1
    'ä':f359, #WS.0+1
    'å':f359, #WS.0+1
    'æ':f359, #WS.0+1
    'ç':f359, #WS.0+1
    'è':f359, #WS.0+1
    'é':f359, #WS.0+1
    'ê':f359, #WS.0+1
    'ë':f359, #WS.0+1
    'ì':f359, #WS.0+1
    'í':f359, #WS.0+1
    'î':f359, #WS.0+1
    'ï':f359, #WS.0+1
    'ð':f359, #WS.0+1
    'ñ':f359, #WS.0+1
    'ò':f359, #WS.0+1
    'ó':f359, #WS.0+1
    'ô':f359, #WS.0+1
    'õ':f359, #WS.0+1
    'ö':f359, #WS.0+1
    '÷':f359, #WS.0+1
    'ø':f359, #WS.0+1
    'ù':f359, #WS.0+1
    'ú':f359, #WS.0+1
    'û':f359, #WS.0+1
    'ü':f359, #WS.0+1
    'ý':f359, #WS.0+1
    'þ':f359, #WS.0+1
    'ÿ':f359, #WS.0+1
    '\\':f3522, #PPN_EP.Bsl
}
Lut1613 = { #IDEN
    'A':f1611, #WS.A+1
    'B':f1611, #WS.A+1
    'C':f1611, #WS.A+1
    'D':f1611, #WS.A+1
    'E':f1611, #WS.A+1
    'F':f1611, #WS.A+1
    'G':f1611, #WS.A+1
    'H':f1611, #WS.A+1
    'I':f1611, #WS.A+1
    'J':f1611, #WS.A+1
    'K':f1611, #WS.A+1
    'L':f1611, #WS.A+1
    'M':f1611, #WS.A+1
    'N':f1611, #WS.A+1
    'O':f1611, #WS.A+1
    'P':f1611, #WS.A+1
    'Q':f1611, #WS.A+1
    'R':f1611, #WS.A+1
    'S':f1611, #WS.A+1
    'T':f1611, #WS.A+1
    'U':f1611, #WS.A+1
    'V':f1611, #WS.A+1
    'W':f1611, #WS.A+1
    'X':f1611, #WS.A+1
    'Y':f1611, #WS.A+1
    'Z':f1611, #WS.A+1
    'a':f1611, #WS.A+1
    'b':f1611, #WS.A+1
    'c':f1611, #WS.A+1
    'd':f1611, #WS.A+1
    'e':f1611, #WS.A+1
    'f':f1611, #WS.A+1
    'g':f1611, #WS.A+1
    'h':f1611, #WS.A+1
    'i':f1611, #WS.A+1
    'j':f1611, #WS.A+1
    'k':f1611, #WS.A+1
    'l':f1611, #WS.A+1
    'm':f1611, #WS.A+1
    'n':f1611, #WS.A+1
    'o':f1611, #WS.A+1
    'p':f1611, #WS.A+1
    'q':f1611, #WS.A+1
    'r':f1611, #WS.A+1
    's':f1611, #WS.A+1
    't':f1611, #WS.A+1
    'u':f1611, #WS.A+1
    'v':f1611, #WS.A+1
    'w':f1611, #WS.A+1
    'x':f1611, #WS.A+1
    'y':f1611, #WS.A+1
    'z':f1611, #WS.A+1
    '_':f1611, #WS.A+1
    '0':f1611, #WS.A+1
    '1':f1611, #WS.A+1
    '2':f1611, #WS.A+1
    '3':f1611, #WS.A+1
    '4':f1611, #WS.A+1
    '5':f1611, #WS.A+1
    '6':f1611, #WS.A+1
    '7':f1611, #WS.A+1
    '8':f1611, #WS.A+1
    '9':f1611, #WS.A+1
    '@':f1611, #WS.A+1
    '$':f1611, #WS.A+1
    '`':f1611, #WS.A+1
    '\x80':f1611, #WS.A+1
    '\x81':f1611, #WS.A+1
    '\x82':f1611, #WS.A+1
    '\x83':f1611, #WS.A+1
    '\x84':f1611, #WS.A+1
    '\x85':f1611, #WS.A+1
    '\x86':f1611, #WS.A+1
    '\x87':f1611, #WS.A+1
    '\x88':f1611, #WS.A+1
    '\x89':f1611, #WS.A+1
    '\x8a':f1611, #WS.A+1
    '\x8b':f1611, #WS.A+1
    '\x8c':f1611, #WS.A+1
    '\x8d':f1611, #WS.A+1
    '\x8e':f1611, #WS.A+1
    '\x8f':f1611, #WS.A+1
    '\x90':f1611, #WS.A+1
    '\x91':f1611, #WS.A+1
    '\x92':f1611, #WS.A+1
    '\x93':f1611, #WS.A+1
    '\x94':f1611, #WS.A+1
    '\x95':f1611, #WS.A+1
    '\x96':f1611, #WS.A+1
    '\x97':f1611, #WS.A+1
    '\x98':f1611, #WS.A+1
    '\x99':f1611, #WS.A+1
    '\x9a':f1611, #WS.A+1
    '\x9b':f1611, #WS.A+1
    '\x9c':f1611, #WS.A+1
    '\x9d':f1611, #WS.A+1
    '\x9e':f1611, #WS.A+1
    '\x9f':f1611, #WS.A+1
    '\xa0':f1611, #WS.A+1
    '¡':f1611, #WS.A+1
    '¢':f1611, #WS.A+1
    '£':f1611, #WS.A+1
    '¤':f1611, #WS.A+1
    '¥':f1611, #WS.A+1
    '¦':f1611, #WS.A+1
    '§':f1611, #WS.A+1
    '¨':f1611, #WS.A+1
    '©':f1611, #WS.A+1
    'ª':f1611, #WS.A+1
    '«':f1611, #WS.A+1
    '¬':f1611, #WS.A+1
    '\xad':f1611, #WS.A+1
    '®':f1611, #WS.A+1
    '¯':f1611, #WS.A+1
    '°':f1611, #WS.A+1
    '±':f1611, #WS.A+1
    '²':f1611, #WS.A+1
    '³':f1611, #WS.A+1
    '´':f1611, #WS.A+1
    'µ':f1611, #WS.A+1
    '¶':f1611, #WS.A+1
    '·':f1611, #WS.A+1
    '¸':f1611, #WS.A+1
    '¹':f1611, #WS.A+1
    'º':f1611, #WS.A+1
    '»':f1611, #WS.A+1
    '¼':f1611, #WS.A+1
    '½':f1611, #WS.A+1
    '¾':f1611, #WS.A+1
    '¿':f1611, #WS.A+1
    'À':f1611, #WS.A+1
    'Á':f1611, #WS.A+1
    'Â':f1611, #WS.A+1
    'Ã':f1611, #WS.A+1
    'Ä':f1611, #WS.A+1
    'Å':f1611, #WS.A+1
    'Æ':f1611, #WS.A+1
    'Ç':f1611, #WS.A+1
    'È':f1611, #WS.A+1
    'É':f1611, #WS.A+1
    'Ê':f1611, #WS.A+1
    'Ë':f1611, #WS.A+1
    'Ì':f1611, #WS.A+1
    'Í':f1611, #WS.A+1
    'Î':f1611, #WS.A+1
    'Ï':f1611, #WS.A+1
    'Ð':f1611, #WS.A+1
    'Ñ':f1611, #WS.A+1
    'Ò':f1611, #WS.A+1
    'Ó':f1611, #WS.A+1
    'Ô':f1611, #WS.A+1
    'Õ':f1611, #WS.A+1
    'Ö':f1611, #WS.A+1
    '×':f1611, #WS.A+1
    'Ø':f1611, #WS.A+1
    'Ù':f1611, #WS.A+1
    'Ú':f1611, #WS.A+1
    'Û':f1611, #WS.A+1
    'Ü':f1611, #WS.A+1
    'Ý':f1611, #WS.A+1
    'Þ':f1611, #WS.A+1
    'ß':f1611, #WS.A+1
    'à':f1611, #WS.A+1
    'á':f1611, #WS.A+1
    'â':f1611, #WS.A+1
    'ã':f1611, #WS.A+1
    'ä':f1611, #WS.A+1
    'å':f1611, #WS.A+1
    'æ':f1611, #WS.A+1
    'ç':f1611, #WS.A+1
    'è':f1611, #WS.A+1
    'é':f1611, #WS.A+1
    'ê':f1611, #WS.A+1
    'ë':f1611, #WS.A+1
    'ì':f1611, #WS.A+1
    'í':f1611, #WS.A+1
    'î':f1611, #WS.A+1
    'ï':f1611, #WS.A+1
    'ð':f1611, #WS.A+1
    'ñ':f1611, #WS.A+1
    'ò':f1611, #WS.A+1
    'ó':f1611, #WS.A+1
    'ô':f1611, #WS.A+1
    'õ':f1611, #WS.A+1
    'ö':f1611, #WS.A+1
    '÷':f1611, #WS.A+1
    'ø':f1611, #WS.A+1
    'ù':f1611, #WS.A+1
    'ú':f1611, #WS.A+1
    'û':f1611, #WS.A+1
    'ü':f1611, #WS.A+1
    'ý':f1611, #WS.A+1
    'þ':f1611, #WS.A+1
    'ÿ':f1611, #WS.A+1
    '\\':f2747, #IDEN.Bsl
}
Lut1644 = { #WS.L+1
    '"':f2845, #WS.L+1.Dq
    "'":f2855, #WS.L+1.Sq
    '\\':f3541, #WS.L+1.Bsl
}
Lut1671 = { #WS.U+1
    '"':f2840, #WS.U+1.Dq
    "'":f2865, #WS.U+1.Sq
    '\\':f3551, #WS.U+1.Bsl
}
Lut1749 = { #WS.u+1
    '8':f2828, #WS.u+1.8
    '"':f2835, #WS.u+1.Dq
    "'":f2860, #WS.u+1.Sq
    '\\':f3561, #WS.u+1.Bsl
}
Lut2163 = { #WS.Bsl+1
    '\n':f25, #WS.Cr.Nl+1
    '\r':f3276, #WS.Bsl+1.Cr
}
Lut2747 = { #IDEN.Bsl
    '\n':f3533, #IDEN.Bsl.Nl
    '\r':f3535, #IDEN.Bsl.Cr
}
Lut2753 = { #IDEN_BS
    'u':f2755, #IDEN_BS.u
    'U':f2760, #IDEN_BS.U
    '\\':f3571, #IDEN_BS.Bsl
}
Lut2758 = { #IDEN_BSU
    '0':f2769, #IDEN_BSU.0
    '1':f2769, #IDEN_BSU.0
    '2':f2769, #IDEN_BSU.0
    '3':f2769, #IDEN_BSU.0
    '4':f2769, #IDEN_BSU.0
    '5':f2769, #IDEN_BSU.0
    '6':f2769, #IDEN_BSU.0
    '7':f2769, #IDEN_BSU.0
    '8':f2769, #IDEN_BSU.0
    '9':f2769, #IDEN_BSU.0
    'A':f2790, #IDEN_BSU.A
    'B':f2790, #IDEN_BSU.A
    'C':f2790, #IDEN_BSU.A
    'D':f2790, #IDEN_BSU.A
    'E':f2790, #IDEN_BSU.A
    'F':f2790, #IDEN_BSU.A
    'a':f2802, #IDEN_BSU.a
    'b':f2802, #IDEN_BSU.a
    'c':f2802, #IDEN_BSU.a
    'd':f2802, #IDEN_BSU.a
    'e':f2802, #IDEN_BSU.a
    'f':f2802, #IDEN_BSU.a
    '\\':f3581, #IDEN_BSU.Bsl
}
Lut2827 = { #QUOT
    "'":f2872, #QUOT.Sq
    '"':f2872, #QUOT.Sq
    '\\':f2879, #QUOT.Bsl
    '\n':f2887, #QUOT.Nl
    '\r':f2891, #QUOT.Cr
    '\x00':f2902, #QUOT.x00
}
Lut2828 = { #WS.u+1.8
    '"':f2830, #WS.u+1.8.Dq
    '\\':f3600, #WS.u+1.8.Bsl
}
Lut2879 = { #QUOT.Bsl
    '\n':f2895, #QUOT.Cr.Nl+2
    '\r':f3594, #QUOT.Bsl.Cr
}
Lut2881 = { #QUOT_BS
    '"':f2905, #QUOT_BS.Dq
    "'":f2905, #QUOT_BS.Dq
    '?':f2905, #QUOT_BS.Dq
    '\\':f2913, #QUOT_BS.Bsl
    'a':f2917, #QUOT_BS.a
    'b':f2920, #QUOT_BS.b
    't':f2923, #QUOT_BS.t
    'n':f2926, #QUOT_BS.n
    'v':f2929, #QUOT_BS.v
    'f':f2932, #QUOT_BS.f
    'r':f2935, #QUOT_BS.r
    '0':f2938, #QUOT_BS.0
    '1':f2938, #QUOT_BS.0
    '2':f2938, #QUOT_BS.0
    '3':f2938, #QUOT_BS.0
    '4':f2938, #QUOT_BS.0
    '5':f2938, #QUOT_BS.0
    '6':f2938, #QUOT_BS.0
    '7':f2938, #QUOT_BS.0
    'x':f3061, #QUOT_BS.x
    'u':f3206, #QUOT_BS.u
    'U':f3211, #QUOT_BS.U
}
Lut2891 = { #QUOT.Cr
    '\n':f2893, #QUOT.Cr.Nl
}
Lut2913 = { #QUOT_BS.Bsl
    '\n':f3611, #QUOT_BS.Bsl.Nl
    '\r':f3613, #QUOT_BS.Bsl.Cr
}
Lut2941 = { #QUOT_BSO1
    '0':f2971, #QUOT_BSO1.0
    '1':f2971, #QUOT_BSO1.0
    '2':f2971, #QUOT_BSO1.0
    '3':f2971, #QUOT_BSO1.0
    '4':f2971, #QUOT_BSO1.0
    '5':f2971, #QUOT_BSO1.0
    '6':f2971, #QUOT_BSO1.0
    '7':f2971, #QUOT_BSO1.0
    '\\':f3619, #QUOT_BSO1.Bsl
}
Lut2975 = { #QUOT_BSO2
    '0':f3013, #QUOT_BSO2.0
    '1':f3013, #QUOT_BSO2.0
    '2':f3013, #QUOT_BSO2.0
    '3':f3013, #QUOT_BSO2.0
    '4':f3013, #QUOT_BSO2.0
    '5':f3013, #QUOT_BSO2.0
    '6':f3013, #QUOT_BSO2.0
    '7':f3013, #QUOT_BSO2.0
    '\\':f3629, #QUOT_BSO2.Bsl
}
Lut3061 = { #QUOT_BS.x
    '0':f3063, #QUOT_BS.x.0
    '1':f3063, #QUOT_BS.x.0
    '2':f3063, #QUOT_BS.x.0
    '3':f3063, #QUOT_BS.x.0
    '4':f3063, #QUOT_BS.x.0
    '5':f3063, #QUOT_BS.x.0
    '6':f3063, #QUOT_BS.x.0
    '7':f3063, #QUOT_BS.x.0
    '8':f3063, #QUOT_BS.x.0
    '9':f3063, #QUOT_BS.x.0
    'A':f3104, #QUOT_BS.x.A
    'B':f3104, #QUOT_BS.x.A
    'C':f3104, #QUOT_BS.x.A
    'D':f3104, #QUOT_BS.x.A
    'E':f3104, #QUOT_BS.x.A
    'F':f3104, #QUOT_BS.x.A
    'a':f3128, #QUOT_BS.x.a
    'b':f3128, #QUOT_BS.x.a
    'c':f3128, #QUOT_BS.x.a
    'd':f3128, #QUOT_BS.x.a
    'e':f3128, #QUOT_BS.x.a
    'f':f3128, #QUOT_BS.x.a
    '\\':f3639, #QUOT_BS.x.Bsl
}
Lut3066 = { #QUOT_BSX
    '0':f3156, #QUOT_BSX.0
    '1':f3156, #QUOT_BSX.0
    '2':f3156, #QUOT_BSX.0
    '3':f3156, #QUOT_BSX.0
    '4':f3156, #QUOT_BSX.0
    '5':f3156, #QUOT_BSX.0
    '6':f3156, #QUOT_BSX.0
    '7':f3156, #QUOT_BSX.0
    '8':f3156, #QUOT_BSX.0
    '9':f3156, #QUOT_BSX.0
    'A':f3177, #QUOT_BSX.A
    'B':f3177, #QUOT_BSX.A
    'C':f3177, #QUOT_BSX.A
    'D':f3177, #QUOT_BSX.A
    'E':f3177, #QUOT_BSX.A
    'F':f3177, #QUOT_BSX.A
    'a':f3189, #QUOT_BSX.a
    'b':f3189, #QUOT_BSX.a
    'c':f3189, #QUOT_BSX.a
    'd':f3189, #QUOT_BSX.a
    'e':f3189, #QUOT_BSX.a
    'f':f3189, #QUOT_BSX.a
    '\\':f3649, #QUOT_BSX.Bsl
}
Lut3209 = { #QUOT_BSU
    '0':f3220, #QUOT_BSU.0
    '1':f3220, #QUOT_BSU.0
    '2':f3220, #QUOT_BSU.0
    '3':f3220, #QUOT_BSU.0
    '4':f3220, #QUOT_BSU.0
    '5':f3220, #QUOT_BSU.0
    '6':f3220, #QUOT_BSU.0
    '7':f3220, #QUOT_BSU.0
    '8':f3220, #QUOT_BSU.0
    '9':f3220, #QUOT_BSU.0
    'A':f3241, #QUOT_BSU.A
    'B':f3241, #QUOT_BSU.A
    'C':f3241, #QUOT_BSU.A
    'D':f3241, #QUOT_BSU.A
    'E':f3241, #QUOT_BSU.A
    'F':f3241, #QUOT_BSU.A
    'a':f3253, #QUOT_BSU.a
    'b':f3253, #QUOT_BSU.a
    'c':f3253, #QUOT_BSU.a
    'd':f3253, #QUOT_BSU.a
    'e':f3253, #QUOT_BSU.a
    'f':f3253, #QUOT_BSU.a
    '\\':f3659, #QUOT_BSU.Bsl
}
Lut3276 = { #WS.Bsl+1.Cr
    '\n':f3278, #WS.Bsl+1.Cr.Nl
}
Lut3282 = { #WS.Sla+1.Bsl
    '\n':f3284, #WS.Sla+1.Bsl.Nl
    '\r':f3286, #WS.Sla+1.Bsl.Cr
}
Lut3286 = { #WS.Sla+1.Bsl.Cr
    '\n':f3288, #WS.Sla+1.Bsl.Cr.Nl
}
Lut3292 = { #SLST.Bsl
    '\n':f59, #SLST.Cr.Nl
    '\r':f3296, #SLST.Bsl.Cr
}
Lut3296 = { #SLST.Bsl.Cr
    '\n':f3298, #SLST.Bsl.Cr.Nl
}
Lut3302 = { #SLSL.Bsl
    '\n':f3304, #SLSL.Bsl.Nl
    '\r':f3306, #SLSL.Bsl.Cr
}
Lut3306 = { #SLSL.Bsl.Cr
    '\n':f3308, #SLSL.Bsl.Cr.Nl
}
Lut3312 = { #SLST.Sta.Bsl
    '\n':f3314, #SLST.Sta.Bsl.Nl
    '\r':f3316, #SLST.Sta.Bsl.Cr
}
Lut3316 = { #SLST.Sta.Bsl.Cr
    '\n':f3318, #SLST.Sta.Bsl.Cr.Nl
}
Lut3322 = { #WS.Dot+1.Bsl
    '\n':f3324, #WS.Dot+1.Bsl.Nl
    '\r':f3326, #WS.Dot+1.Bsl.Cr
}
Lut3326 = { #WS.Dot+1.Bsl.Cr
    '\n':f3328, #WS.Dot+1.Bsl.Cr.Nl
}
Lut3332 = { #WS.Min+1.Bsl
    '\n':f3334, #WS.Min+1.Bsl.Nl
    '\r':f3336, #WS.Min+1.Bsl.Cr
}
Lut3336 = { #WS.Min+1.Bsl.Cr
    '\n':f3338, #WS.Min+1.Bsl.Cr.Nl
}
Lut3342 = { #WS.Plu+1.Bsl
    '\n':f3344, #WS.Plu+1.Bsl.Nl
    '\r':f3346, #WS.Plu+1.Bsl.Cr
}
Lut3346 = { #WS.Plu+1.Bsl.Cr
    '\n':f3348, #WS.Plu+1.Bsl.Cr.Nl
}
Lut3352 = { #WS.Amp+1.Bsl
    '\n':f3354, #WS.Amp+1.Bsl.Nl
    '\r':f3356, #WS.Amp+1.Bsl.Cr
}
Lut3356 = { #WS.Amp+1.Bsl.Cr
    '\n':f3358, #WS.Amp+1.Bsl.Cr.Nl
}
Lut3362 = { #WS.Sta+1.Bsl
    '\n':f3364, #WS.Sta+1.Bsl.Nl
    '\r':f3366, #WS.Sta+1.Bsl.Cr
}
Lut3366 = { #WS.Sta+1.Bsl.Cr
    '\n':f3368, #WS.Sta+1.Bsl.Cr.Nl
}
Lut3372 = { #WS.Exc+1.Bsl
    '\n':f3374, #WS.Exc+1.Bsl.Nl
    '\r':f3376, #WS.Exc+1.Bsl.Cr
}
Lut3376 = { #WS.Exc+1.Bsl.Cr
    '\n':f3378, #WS.Exc+1.Bsl.Cr.Nl
}
Lut3382 = { #WS.Per+1.Bsl
    '\n':f3384, #WS.Per+1.Bsl.Nl
    '\r':f3386, #WS.Per+1.Bsl.Cr
}
Lut3386 = { #WS.Per+1.Bsl.Cr
    '\n':f3388, #WS.Per+1.Bsl.Cr.Nl
}
Lut3392 = { #WS.Lt+1.Bsl
    '\n':f3394, #WS.Lt+1.Bsl.Nl
    '\r':f3396, #WS.Lt+1.Bsl.Cr
}
Lut3396 = { #WS.Lt+1.Bsl.Cr
    '\n':f3398, #WS.Lt+1.Bsl.Cr.Nl
}
Lut3402 = { #WS.Lt+1.Lt.Bsl
    '\n':f3404, #WS.Lt+1.Lt.Bsl.Nl
    '\r':f3406, #WS.Lt+1.Lt.Bsl.Cr
}
Lut3406 = { #WS.Lt+1.Lt.Bsl.Cr
    '\n':f3408, #WS.Lt+1.Lt.Bsl.Cr.Nl
}
Lut3412 = { #WS.Gt+1.Bsl
    '\n':f3414, #WS.Gt+1.Bsl.Nl
    '\r':f3416, #WS.Gt+1.Bsl.Cr
}
Lut3416 = { #WS.Gt+1.Bsl.Cr
    '\n':f3418, #WS.Gt+1.Bsl.Cr.Nl
}
Lut3422 = { #WS.Gt+1.Gt.Bsl
    '\n':f3424, #WS.Gt+1.Gt.Bsl.Nl
    '\r':f3426, #WS.Gt+1.Gt.Bsl.Cr
}
Lut3426 = { #WS.Gt+1.Gt.Bsl.Cr
    '\n':f3428, #WS.Gt+1.Gt.Bsl.Cr.Nl
}
Lut3432 = { #WS.Equ+1.Bsl
    '\n':f3434, #WS.Equ+1.Bsl.Nl
    '\r':f3436, #WS.Equ+1.Bsl.Cr
}
Lut3436 = { #WS.Equ+1.Bsl.Cr
    '\n':f3438, #WS.Equ+1.Bsl.Cr.Nl
}
Lut3442 = { #WS.Car+1.Bsl
    '\n':f3444, #WS.Car+1.Bsl.Nl
    '\r':f3446, #WS.Car+1.Bsl.Cr
}
Lut3446 = { #WS.Car+1.Bsl.Cr
    '\n':f3448, #WS.Car+1.Bsl.Cr.Nl
}
Lut3452 = { #WS.Bar+1.Bsl
    '\n':f3454, #WS.Bar+1.Bsl.Nl
    '\r':f3456, #WS.Bar+1.Bsl.Cr
}
Lut3456 = { #WS.Bar+1.Bsl.Cr
    '\n':f3458, #WS.Bar+1.Bsl.Cr.Nl
}
Lut3462 = { #WS.Col+1.Bsl
    '\n':f3464, #WS.Col+1.Bsl.Nl
    '\r':f3466, #WS.Col+1.Bsl.Cr
}
Lut3466 = { #WS.Col+1.Bsl.Cr
    '\n':f3468, #WS.Col+1.Bsl.Cr.Nl
}
Lut3472 = { #WS.Dot+1.Dot+1.Bsl
    '\n':f3474, #WS.Dot+1.Dot+1.Bsl.Nl
    '\r':f3476, #WS.Dot+1.Dot+1.Bsl.Cr
}
Lut3476 = { #WS.Dot+1.Dot+1.Bsl.Cr
    '\n':f3478, #WS.Dot+1.Dot+1.Bsl.Cr.Nl
}
Lut3482 = { #WS.Has+1.Bsl
    '\n':f3484, #WS.Has+1.Bsl.Nl
    '\r':f3486, #WS.Has+1.Bsl.Cr
}
Lut3486 = { #WS.Has+1.Bsl.Cr
    '\n':f3488, #WS.Has+1.Bsl.Cr.Nl
}
Lut3492 = { #WS.Per+1.Col.Bsl
    '\n':f3494, #WS.Per+1.Col.Bsl.Nl
    '\r':f3496, #WS.Per+1.Col.Bsl.Cr
}
Lut3496 = { #WS.Per+1.Col.Bsl.Cr
    '\n':f3498, #WS.Per+1.Col.Bsl.Cr.Nl
}
Lut3502 = { #WS.Per+1.Col.Per+1.Bsl
    '\n':f3504, #WS.Per+1.Col.Per+1.Bsl.Nl
    '\r':f3506, #WS.Per+1.Col.Per+1.Bsl.Cr
}
Lut3506 = { #WS.Per+1.Col.Per+1.Bsl.Cr
    '\n':f3508, #WS.Per+1.Col.Per+1.Bsl.Cr.Nl
}
Lut3512 = { #PPN_1.Bsl
    '\n':f3514, #PPN_1.Bsl.Nl
    '\r':f3516, #PPN_1.Bsl.Cr
}
Lut3516 = { #PPN_1.Bsl.Cr
    '\n':f3518, #PPN_1.Bsl.Cr.Nl
}
Lut3522 = { #PPN_EP.Bsl
    '\n':f3524, #PPN_EP.Bsl.Nl
    '\r':f3526, #PPN_EP.Bsl.Cr
}
Lut3526 = { #PPN_EP.Bsl.Cr
    '\n':f3528, #PPN_EP.Bsl.Cr.Nl
}
Lut3535 = { #IDEN.Bsl.Cr
    '\n':f3537, #IDEN.Bsl.Cr.Nl
}
Lut3541 = { #WS.L+1.Bsl
    '\n':f3543, #WS.L+1.Bsl.Nl
    '\r':f3545, #WS.L+1.Bsl.Cr
}
Lut3545 = { #WS.L+1.Bsl.Cr
    '\n':f3547, #WS.L+1.Bsl.Cr.Nl
}
Lut3551 = { #WS.U+1.Bsl
    '\n':f3553, #WS.U+1.Bsl.Nl
    '\r':f3555, #WS.U+1.Bsl.Cr
}
Lut3555 = { #WS.U+1.Bsl.Cr
    '\n':f3557, #WS.U+1.Bsl.Cr.Nl
}
Lut3561 = { #WS.u+1.Bsl
    '\n':f3563, #WS.u+1.Bsl.Nl
    '\r':f3565, #WS.u+1.Bsl.Cr
}
Lut3565 = { #WS.u+1.Bsl.Cr
    '\n':f3567, #WS.u+1.Bsl.Cr.Nl
}
Lut3571 = { #IDEN_BS.Bsl
    '\n':f3573, #IDEN_BS.Bsl.Nl
    '\r':f3575, #IDEN_BS.Bsl.Cr
}
Lut3575 = { #IDEN_BS.Bsl.Cr
    '\n':f3577, #IDEN_BS.Bsl.Cr.Nl
}
Lut3581 = { #IDEN_BSU.Bsl
    '\n':f3583, #IDEN_BSU.Bsl.Nl
    '\r':f3585, #IDEN_BSU.Bsl.Cr
}
Lut3585 = { #IDEN_BSU.Bsl.Cr
    '\n':f3587, #IDEN_BSU.Bsl.Cr.Nl
}
Lut3594 = { #QUOT.Bsl.Cr
    '\n':f3596, #QUOT.Bsl.Cr.Nl
}
Lut3600 = { #WS.u+1.8.Bsl
    '\n':f3602, #WS.u+1.8.Bsl.Nl
    '\r':f3604, #WS.u+1.8.Bsl.Cr
}
Lut3604 = { #WS.u+1.8.Bsl.Cr
    '\n':f3606, #WS.u+1.8.Bsl.Cr.Nl
}
Lut3613 = { #QUOT_BS.Bsl.Cr
    '\n':f3615, #QUOT_BS.Bsl.Cr.Nl
}
Lut3619 = { #QUOT_BSO1.Bsl
    '\n':f3621, #QUOT_BSO1.Bsl.Nl
    '\r':f3623, #QUOT_BSO1.Bsl.Cr
}
Lut3623 = { #QUOT_BSO1.Bsl.Cr
    '\n':f3625, #QUOT_BSO1.Bsl.Cr.Nl
}
Lut3629 = { #QUOT_BSO2.Bsl
    '\n':f3631, #QUOT_BSO2.Bsl.Nl
    '\r':f3633, #QUOT_BSO2.Bsl.Cr
}
Lut3633 = { #QUOT_BSO2.Bsl.Cr
    '\n':f3635, #QUOT_BSO2.Bsl.Cr.Nl
}
Lut3639 = { #QUOT_BS.x.Bsl
    '\n':f3641, #QUOT_BS.x.Bsl.Nl
    '\r':f3643, #QUOT_BS.x.Bsl.Cr
}
Lut3643 = { #QUOT_BS.x.Bsl.Cr
    '\n':f3645, #QUOT_BS.x.Bsl.Cr.Nl
}
Lut3649 = { #QUOT_BSX.Bsl
    '\n':f3651, #QUOT_BSX.Bsl.Nl
    '\r':f3653, #QUOT_BSX.Bsl.Cr
}
Lut3653 = { #QUOT_BSX.Bsl.Cr
    '\n':f3655, #QUOT_BSX.Bsl.Cr.Nl
}
Lut3659 = { #QUOT_BSU.Bsl
    '\n':f3661, #QUOT_BSU.Bsl.Nl
    '\r':f3663, #QUOT_BSU.Bsl.Cr
}
Lut3663 = { #QUOT_BSU.Bsl.Cr
    '\n':f3665, #QUOT_BSU.Bsl.Cr.Nl
}
START = f4
WS = f5
SLST = f45
SLSL = f48
PPN_1 = f361
PPN_EP = f1005
PPN_FIN = f1607
IDEN = f1613
IDEN_BS_0 = f2752
IDEN_BS = f2753
IDEN_BSU = f2758
IDEN_BSU_NEXT = f2813
IDEN_BSU_FIN = f2821
QUOT = f2827
QUOT_FIN = f40
QUOT_BS = f2881
QUOT_BSO1 = f2941
QUOT_BSO2 = f2975
QUOT_BSX = f3066
QUOT_BSX_NEXT = f3201
QUOT_BSU = f3209
QUOT_BSU_NEXT = f3264
QUOT_BSU_FIN = f3011
