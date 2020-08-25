#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import re
import math


def main():
    nScore = nLength = nAlphaUC = nAlphaLC = nNumber = nSymbol = nMidChar = nRequirements = nAlphasOnly = nNumbersOnly = nUnqChar = nRepChar = nRepInc = nConsecAlphaUC = nConsecAlphaLC = nConsecNumber = nConsecSymbol = nConsecCharType = nSeqAlpha = nSeqNumber = nSeqSymbol = nSeqChar = nReqChar = nMultConsecCharType = 0
    nMultRepChar = nMultConsecSymbol = 1
    nMultMidChar = nMultRequirements = nMultConsecAlphaUC = nMultConsecAlphaLC = nMultConsecNumber = 2
    nReqCharType = nMultAlphaUC = nMultAlphaLC = nMultSeqAlpha = nMultSeqNumber = nMultSeqSymbol = 3
    nMultLength = nMultNumber = 4
    nMultSymbol = 6
    nTmpAlphaUC = nTmpAlphaLC = nTmpNumber = nTmpSymbol = ""
    sAlphaUC = sAlphaLC = sNumber = sSymbol = sMidChar = sRequirements = sAlphasOnly = sNumbersOnly = sRepChar = sConsecAlphaUC = sConsecAlphaLC = sConsecNumber = sSeqAlpha = sSeqNumber = sSeqSymbol = "0"
    sAlphas = "abcdefghijklmnopqrstuvwxyz"
    sNumerics = "01234567890"
    sSymbols = ")!@#$%^&*()"

    # check argv exists or not
    pwd = sys.argv[1]
    nLength = len(pwd)
    nScore = nLength * nMultLength
    arrPwd = list(pwd)
    arrPwdLen = len(arrPwd)

    # Check Uppercase, Lowercase, Numeric and Symbol
    for a in range(0, arrPwdLen):
        if re.match(r'[A-Z]', arrPwd[a]):
            if nTmpAlphaUC != "":
                if (nTmpAlphaUC + 1) == a:
                    nConsecAlphaUC += 1
                    nConsecCharType += 1
            nTmpAlphaUC = a
            nAlphaUC += 1
        elif re.match(r'[a-z]', arrPwd[a]):
            if nTmpAlphaLC != "":
                if (nTmpAlphaLC + 1) == a:
                    nConsecAlphaLC += 1
                    nConsecCharType += 1
            nTmpAlphaLC = a
            nAlphaLC += 1
        elif re.match(r'[0-9]', arrPwd[a]):
            if a > 0 and a < (arrPwdLen - 1):
                nMidChar += 1
            if nTmpNumber != "":
                if (nTmpNumber + 1) == a:
                    nConsecNumber += 1
                    nConsecCharType += 1
            nTmpNumber = a
            nNumber += 1
        elif re.match(r'[^a-zA-Z0-9_]', arrPwd[a]):
            if a > 0 and a < (arrPwdLen - 1):
                nMidChar += 1
            if nTmpSymbol != "":
                if (nTmpSymbol+1) == a:
                    nConsecSymbol += 1
                    nConsecCharType += 1
            nTmpSymbol = a
            nSymbol += 1

        # Check for repeat characters
        bCharExists = False
        for b in range(0, arrPwdLen):
            if arrPwd[a] == arrPwd[b] and a != b:
                bCharExists = True
                nRepInc += abs(arrPwdLen/(b-a))

        if bCharExists:
            nRepChar += 1
            nUnqChar = arrPwdLen - nRepChar
            nRepInc = math.ceil(nRepInc/nUnqChar) if nUnqChar else math.ceil(nRepInc)

    # Check for sequential alpha string patterns (forward and reverse)
    for s in range(0, 24):
        sFwd = sAlphas[s:s+3]
        sRev = sFwd[::-1]
        if pwd.lower().find(sFwd) != -1 or pwd.lower().find(sRev) != -1:
            nSeqAlpha += 1
            nSeqChar += 1

    # Check for sequential numeric string patterns (forward and reverse)
    for s in range(0, 9):
        sFwd = sNumerics[s:s+3]
        sRev = sFwd[::-1]
        if pwd.lower().find(sFwd) != -1 or pwd.lower().find(sRev) != -1:
            nSeqNumber += 1
            nSeqChar += 1

    # Check for sequential symbol string patterns (forward and reverse)
    for s in range(0, 9):
        sFwd = sSymbols[s:s+3]
        sRev = sFwd[::-1]
        if pwd.lower().find(sFwd) != -1 or pwd.lower().find(sRev) != -1:
            nSeqSymbol += 1
            nSeqChar += 1

    # General point assignment
    if nAlphaUC > 0 and nAlphaUC < nLength:
        nScore += (nLength - nAlphaUC) * 2
        sAlphaUC = "+" + str((nLength - nAlphaUC) * 2)

    if nAlphaLC > 0 and nAlphaLC < nLength:
        nScore += (nLength - nAlphaLC) * 2
        sAlphaLC = "+" + str((nLength - nAlphaLC) * 2)

    if nNumber > 0 and nNumber < nLength:
        nScore += nNumber * nMultNumber
        sNumber = "+" + str(nNumber * nMultNumber)

    if nSymbol > 0:
        nScore += nSymbol * nMultSymbol
        sSymbol = "+" + str(nSymbol * nMultSymbol)

    if nMidChar > 0:
        nScore += nMidChar * nMultMidChar
        sMidChar = "+" + str(nMidChar * nMultMidChar)

    # Point deductions
    if (nAlphaLC > 0 or nAlphaUC > 0) and nSymbol == 0 and nNumber == 0:
        nScore -= nLength
        nAlphasOnly = nLength
        sAlphasOnly = "-" + str(nLength)

    if nAlphaLC == 0 and nAlphaUC == 0 and nSymbol == 0 and nNumber == 0:
        nScore -= nLength
        nNumbersOnly = nLength
        sNumbersOnly = "-" + str(nLength)

    if nRepChar > 0:
        nScore -= nRepInc
        sRepChar = "-"+str(nRepInc)

    if nConsecAlphaUC > 0:
        nScore -= nConsecAlphaUC * nMultConsecAlphaUC
        sConsecAlphaUC = "-" + str(nConsecAlphaUC * nMultConsecAlphaUC)

    if nConsecAlphaLC > 0:
        nScore -= nConsecAlphaLC * nMultConsecAlphaLC
        sConsecAlphaLC = "-" + str(nConsecAlphaLC * nMultConsecAlphaLC)

    if nConsecNumber > 0:
        nScore -= nConsecNumber * nMultConsecNumber
        sConsecNumber = "-" + str(nConsecNumber * nMultConsecNumber)

    # line 212 http://www.passwordmeter.com/js/pwdmeter.js


if __name__ == '__main__':
    main()
