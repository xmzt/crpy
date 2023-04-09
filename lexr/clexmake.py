import cbase
import chtab
import logclib

from pylib0_xmzt import loglib

import sys

#======================================================================================================================
# logging, diagnostics, round 2 of imports
#
# g_logc must be set up before importing modules that 'from __main__ import g_logc' in order to
# support decorators conditional on g_logc.

# sys.argv processing that affects g_logc must happen before such imports. Currently I find it
# adequate to just modify the line below and rerun rather than parse sys.argv.

logr = loglib.Logr5File()
g_logc = logclib.g_logc = logclib.Logc().logrSet(logr).dumpNodeTreeInit('t.nodetree.log.').kvSet(
    err=1, chain=0, code=0, dumpNodeTreePhase=0, eva=0, insert=0, off=0, phase=1, scan=0, scope=0, unredun=0,
)

import machlib

#======================================================================================================================
# grammar

def gram0(mach):
    mach.parse(r'''
    (@ = id0     [A-Za-z_@$\`\x80-\xFF])
    (@ = id1     [A-Za-z_0-9@$\`\x80-\xFF])
    (@ = ppn1All [A-Za-z_0-9.@$\`\x80-\xFF])
    (@ = ppnEp1  [A-Za-z_0-9.+\-@$\`\x80-\xFF])
    (@ = ppnEp   [eEpP])
    (@ = ppn1Nep (- ppn1All ppnEp))
    (@ = wsH     [ \t\v\f])
    (@ = eolV    (list '\n' '\r\n' '\r'))
    (@ = bs      '\\')
    (@ = nul     '\0')
    (@ = wsAll   [\0- \x7f])

    # run-time global symbols
    (@ sym AccTyp)
    (@ sym TokErr)
    (@ sym TokTyp)
    (@ sym Ws)

    # run-time members token
    (@ mem accTyp)
    (@ mem tokSrc srcPtr)
    (@ mem tokTyp)
    (@ mem tokWs)

    # run-time members temporary
    (@ mem bsuI int)
    (@ mem quoteCh str)
    (@ mem srcTmp0 srcPtr)
    (@ mem tmpU int)
    (@ mem tmpV int)

    # run-time methods
    (@ mem acc None None str)
    (@ mem errPos)
    (@ mem errText)
    (@ mem tokAdd)
    (@ mem tokAddAcc)
    
    #------------------------------------------------------------------------------------------------------------------
    # whitespace

    START     (off= 0) (= tokWs Ws._0) WS
    WS wsH    (|= tokWs Ws.H) (src+) WS
    (@ = condNemptyEn 0) WS (for eol eolV)  (|= tokWs Ws.Eol) (src+) (line+) WS
    WS nul    (= tokSrc src) (|= tokWs Ws.Eol Ws.Eof) (= tokTyp TokTyp.Eof) (tokAdd) (term)
    WS *      (= tokSrc src) (acc *src) (= accTyp AccTyp._0) (= tokTyp TokTyp.Other) (tokAddAcc) (src+) START

    #------------------------------------------------------------------------------------------------------------------
    # comments

    WS '/*'              (src+) SLST
    WS '//'              (src+) SLSL
        
    SLST '*/'            (|= tokWs Ws.H) (src+) WS
    SLST '*'             (src+) SLST
    (@ = condNemptyEn 0) SLST (for eol eolV)  (src+) (line+) SLST
    SLST *               (src+) SLST

    (@ = condNemptyEn 0) SLSL (for eol eolV)  (|= tokWs Ws.Eol) (src+) (line+) WS
    SLSL *               (src+) SLSL
    ''')
    
    for x in cbase.PuncV:
        mach.parse(f'WS {x!r} PUNC_{chtab.name(x)} (= tokTyp TokTyp.{chtab.name(x)}) (tokAdd) (src+) WS')

    mach.parse(r'''
    WS '..' (insert) (= srcTmp0 src)
    WS '..' PUNC_Dot_Dot (= tokTyp TokTyp.Dot) (tokAdd) (src+ 1) (= tokSrc (+ srcTmp0 1)) WS.to.Dot

    WS '%:%' (insert) (= srcTmp0 src)
    WS '%:%' PUNC_Per_Col_Per (= tokTyp TokTyp.Per_Col) (tokAdd) (src+ 2) (= tokSrc (+ srcTmp0 2)) WS.to.Per

    #------------------------------------------------------------------------------------------------------------------
    # ppnumber

    WS [0-9]       (acc *src) (src+) PPN_1
    WS '.' [0-9]   (acc '.') (acc *src) (src+) PPN_1
    PPN_1 ppn1Nep  (acc *src) (src+) PPN_1
    PPN_1 ppnEp    (acc *src) (src+) PPN_EP
    PPN_1          PPN_FIN
    PPN_EP ppnEp1  (acc *src) (src+) PPN_1
    PPN_EP         PPN_FIN
    PPN_FIN        (= accTyp AccTyp._0) (= tokTyp TokTyp.Ppn) (tokAddAcc) START

    #------------------------------------------------------------------------------------------------------------------
    # identifier

    WS id0            (acc *src) (src+) IDEN
    WS bs             IDEN_BS_0

    IDEN id1          (acc *src) (src+) IDEN
    IDEN bs           IDEN_BS_0
    IDEN              IDEN_FIN (= accTyp AccTyp._0) (= tokTyp TokTyp.Iden) (tokAddAcc) START

    IDEN_BS_0         (= srcTmp0 src) IDEN_BS
    IDEN_BS 'u'       (= bsuI 4) (= tmpU 0) (src+) IDEN_BSU
    IDEN_BS 'U'       (= bsuI 8) (= tmpU 0) (src+) IDEN_BSU
    IDEN_BS           IDEN_BS_ERR (errText srcTmp0 src TokErr.BsEscapeInvalid) (src<- srcTmp0) (acc bs) (src+) IDEN
    IDEN_BSU [0-9]    (= tmpV '0') IDEN_BSU_NEXT
    IDEN_BSU [A-F]    (= tmpV 'A') IDEN_BSU_NEXT
    IDEN_BSU [a-f]    (= tmpV 'a') IDEN_BSU_NEXT
    IDEN_BSU          IDEN_BS_ERR
    IDEN_BSU_NEXT     (*= tmpU 16) (+= tmpU *src) (-= tmpU tmpV) (src+) \
                      (-= bsuI 1) (if (== 0 bsuI) IDEN_BSU_FIN) IDEN_BSU
    IDEN_BSU_FIN      (acc tmpU) IDEN

    WS '"'            (= accTyp AccTyp._0) (= tokTyp TokTyp.Sl) (= quoteCh *src) (src+) QUOT
    WS 'u8"'          (= accTyp AccTyp.u8) (= tokTyp TokTyp.Sl) (= quoteCh *src) (src+) QUOT
    WS 'u"'           (= accTyp AccTyp.u)  (= tokTyp TokTyp.Sl) (= quoteCh *src) (src+) QUOT
    WS 'U"'           (= accTyp AccTyp.U)  (= tokTyp TokTyp.Sl) (= quoteCh *src) (src+) QUOT
    WS 'L"'           (= accTyp AccTyp.L)  (= tokTyp TokTyp.Sl) (= quoteCh *src) (src+) QUOT
    WS "'"            (= accTyp AccTyp._0) (= tokTyp TokTyp.Cc) (= quoteCh *src) (src+) QUOT
    WS "L'"           (= accTyp AccTyp.L)  (= tokTyp TokTyp.Cc) (= quoteCh *src) (src+) QUOT
    WS "u'"           (= accTyp AccTyp.u)  (= tokTyp TokTyp.Cc) (= quoteCh *src) (src+) QUOT
    WS "U'"           (= accTyp AccTyp.U)  (= tokTyp TokTyp.Cc) (= quoteCh *src) (src+) QUOT
    WS 'u8'           (acc 'u8') (src+) IDEN
    
    QUOT ['"]         (if (== quoteCh *src) QUOT_FIN) QUOT_ACC
    QUOT bs           (= srcTmp0 src) QUOT_BS
    QUOT *            QUOT_ACC (acc *src) (src+) QUOT
    QUOT_FIN          (tokAddAcc) (src+) START

    (@ = condNemptyEn 0) QUOT (for eol eolV) (errPos src TokErr.QuotEol) (acc eol) (src+) (line+) QUOT
    QUOT nul !        (errPos src TokErr.QuotEof) (tokAddAcc) START
    
    QUOT_BS '"'       (acc *src) (src+) QUOT
    QUOT_BS "'"       (acc *src) (src+) QUOT
    QUOT_BS '?'       (acc *src) (src+) QUOT
    QUOT_BS bs        (acc *src) (src+) QUOT
    QUOT_BS 'a'       (acc '\a') (src+) QUOT
    QUOT_BS 'b'       (acc '\b') (src+) QUOT
    QUOT_BS 't'       (acc '\t') (src+) QUOT
    QUOT_BS 'n'       (acc '\n') (src+) QUOT
    QUOT_BS 'v'       (acc '\v') (src+) QUOT
    QUOT_BS 'f'       (acc '\f') (src+) QUOT
    QUOT_BS 'r'       (acc '\r') (src+) QUOT
    
    QUOT_BS [0-7]     (= tmpU *src) (-= tmpU '0') (src+) QUOT_BSO1
    QUOT_BSO1 [0-7]   (*= tmpU 8) (+= tmpU *src) (-= tmpU '0') (src+) QUOT_BSO2
    QUOT_BSO1         (acc tmpU) QUOT
    QUOT_BSO2 [0-7]   (*= tmpU 8) (+= tmpU *src) (-= tmpU '0') (src+) (acc tmpU) QUOT
    QUOT_BSO2         (acc tmpU) QUOT

    QUOT_BS 'x' [0-9] (= tmpU *src) (-= tmpU '0') (src+) QUOT_BSX
    QUOT_BS 'x' [A-F] (= tmpU *src) (-= tmpU 'A') (src+) QUOT_BSX
    QUOT_BS 'x' [a-f] (= tmpU *src) (-= tmpU 'a') (src+) QUOT_BSX
    QUOT_BS 'x'       (errText srcTmp0 src TokErr.BsEscapeInvalid) (src<- srcTmp0) (acc bs) (src+) QUOT
    QUOT_BSX [0-9]    (= tmpV '0') QUOT_BSX_NEXT
    QUOT_BSX [A-F]    (= tmpV 'A') QUOT_BSX_NEXT
    QUOT_BSX [a-f]    (= tmpV 'a') QUOT_BSX_NEXT
    QUOT_BSX          (acc tmpU) QUOT
    QUOT_BSX_NEXT     (*= tmpU 16) (+= tmpU *src) (-= tmpU tmpV) (src+) QUOT_BSX
    
    QUOT_BS 'u'       (= bsuI 4) (= tmpU 0) (src+) QUOT_BSU
    QUOT_BS 'U'       (= bsuI 8) (= tmpU 0) (src+) QUOT_BSU
    QUOT_BS           QUOT_BS_ERR (errText srcTmp0 src TokErr.BsEscapeInvalid) (src<- srcTmp0) (acc bs) (src+) QUOT
    QUOT_BSU [0-9]    (= tmpV '0') QUOT_BSU_NEXT
    QUOT_BSU [A-F]    (= tmpV 'A') QUOT_BSU_NEXT
    QUOT_BSU [a-f]    (= tmpV 'a') QUOT_BSU_NEXT
    QUOT_BSU          QUOT_BS_ERR
    QUOT_BSU_NEXT     (*= tmpU 16) (+= tmpU *src) (-= tmpU tmpV) (src+) \
                      (-= bsuI 1) (if (== 0 bsuI) QUOT_BSU_FIN) QUOT_BSU
    QUOT_BSU_FIN      (acc tmpU) QUOT

    WS (- (WS.to.chset) wsAll) (insert) (= tokSrc src)
    (@ = condV (mach.condNemptyV))
    (for node0 condV) bs (for eol eolV) (src+from node0) (line+) node0
    (for node0 condV) bs ? (off- 1) (sameTo node0)
    ''')

# grammar end
#======================================================================================================================

machlib.Mach.compilFromGram(sys.argv[1], gram0)
