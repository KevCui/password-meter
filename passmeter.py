#!/usr/bin/python3
# -*- coding: utf-8 -*-
from getpass import getpass
from rich.console import Console
from rich.table import Table
from rich.text import Text
import sys
import re
import math
import argparse


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--password', nargs=1, help='Password')
    parser.add_argument('-s', '--score-only', action='store_true', help='Only show score number as output')
    return parser.parse_args()


def calcResult(score):
    if score < 20:
        return str(max(score, 0)) + "%", "Very Weak"
    if score >= 20 and score < 40:
        return str(score) + "%", "Weak"
    if score >= 40 and score < 60:
        return str(score) + "%", "Good"
    if score >= 60 and score < 80:
        return str(score) + "%", "Strong"
    if score >= 80:
        return str(min(score, 100)) + "%", "Very Strong"
    return 'n/a', 'Unknown'


def setBonuscolor(score):
    if score > 0:
        return Text("+" + str(score), style="green")
    if score < 0:
        return Text(str(score), style="red")
    return Text("0", style="white")


def main():
    args = parseArgs()

    nScore = nLength = nAlphaUC = nAlphaLC = nNumber = nSymbol = nMidChar = nRequirements = nAlphasOnly = nNumbersOnly = nUnqChar = nRepChar = nRepInc = nConsecAlphaUC = nConsecAlphaLC = nConsecNumber = nConsecSymbol = nConsecCharType = nSeqAlpha = nSeqNumber = nSeqSymbol = nSeqChar = 0
    nMultMidChar = nMultRequirements = nMultAlphaUC = nMultAlphaLC = nMultConsecAlphaUC = nMultConsecAlphaLC = nMultConsecNumber = 2
    nMultSeqAlpha = nMultSeqNumber = nMultSeqSymbol = 3
    nMultLength = nMultNumber = 4
    nMultSymbol = 6
    nTmpAlphaUC = nTmpAlphaLC = nTmpNumber = nTmpSymbol = ""
    sAlphaUC = sAlphaLC = sNumber = sSymbol = sMidChar = sRequirements = sAlphasOnly = sNumbersOnly = sRepChar = sConsecAlphaUC = sConsecAlphaLC = sConsecNumber = sSeqAlpha = sSeqNumber = sSeqSymbol = 0
    sAlphas = "abcdefghijklmnopqrstuvwxyz"
    sNumerics = "01234567890"
    sSymbols = ")!@#$%^&*()"
    nMinPwdLen = 8
    nMinReqChars = 4
    if args.password:
        pwd = args.password[0]
    else:
        try:
            pwd = getpass()
        except KeyboardInterrupt:
            sys.exit(1)
    nLength = len(pwd)
    arrPwd = list(pwd)
    arrPwdLen = len(arrPwd)
    sLength = nLength * nMultLength
    nScore = nLength * nMultLength

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
        nScore += (nLength - nAlphaUC) * nMultAlphaUC
        sAlphaUC = (nLength - nAlphaUC) * nMultAlphaUC

    if nAlphaLC > 0 and nAlphaLC < nLength:
        nScore += (nLength - nAlphaLC) * nMultAlphaLC
        sAlphaLC = (nLength - nAlphaLC) * nMultAlphaLC

    if nNumber > 0 and nNumber < nLength:
        nScore += nNumber * nMultNumber
        sNumber = nNumber * nMultNumber

    if nSymbol > 0:
        nScore += nSymbol * nMultSymbol
        sSymbol = nSymbol * nMultSymbol

    if nMidChar > 0:
        nScore += nMidChar * nMultMidChar
        sMidChar = nMidChar * nMultMidChar

    # Point deductions
    if (nAlphaLC > 0 or nAlphaUC > 0) and nSymbol == 0 and nNumber == 0:
        nScore -= nLength
        nAlphasOnly = nLength
        sAlphasOnly = nLength * -1

    if nAlphaLC == 0 and nAlphaUC == 0 and nSymbol == 0 and nNumber > 0:
        nScore -= nLength
        nNumbersOnly = nLength
        sNumbersOnly = nLength * -1

    if nRepChar > 0:
        nScore -= nRepInc
        sRepChar = nRepInc * -1

    if nConsecAlphaUC > 0:
        nScore -= nConsecAlphaUC * nMultConsecAlphaUC
        sConsecAlphaUC = nConsecAlphaUC * nMultConsecAlphaUC * -1

    if nConsecAlphaLC > 0:
        nScore -= nConsecAlphaLC * nMultConsecAlphaLC
        sConsecAlphaLC = nConsecAlphaLC * nMultConsecAlphaLC * -1

    if nConsecNumber > 0:
        nScore -= nConsecNumber * nMultConsecNumber
        sConsecNumber = nConsecNumber * nMultConsecNumber * -1

    if nSeqAlpha > 0:
        nScore -= nSeqAlpha * nMultSeqAlpha
        sSeqAlpha = nSeqAlpha * nMultSeqAlpha * -1

    if nSeqNumber > 0:
        nScore -= nSeqNumber * nMultSeqNumber
        sSeqNumber = nSeqNumber * nMultSeqNumber * -1

    if nSeqSymbol > 0:
        nScore -= nSeqSymbol * nMultSeqSymbol
        sSeqSymbol = nSeqSymbol * nMultSeqSymbol * -1

    # Determine if mandatory requirements have been met
    arrChars = [nAlphaUC, nAlphaLC, nNumber, nSymbol]
    for c in arrChars:
        if c > 0:
            nRequirements += 1

    if nLength >= nMinPwdLen:
        nRequirements += 1
        if nRequirements >= nMinReqChars:
            nScore += nRequirements * nMultRequirements
            sRequirements = nRequirements * nMultRequirements

    fScore, fComplexity = calcResult(nScore)
    if args.score_only:
        print(fScore)
    else:
        print("Score: " + fScore)
        print("Complexity: " + fComplexity)

        table = Table()
        table.add_column("", style="cyan")
        table.add_column("Rate", style="white")
        table.add_column("Count", justify="right", style="yellow")
        table.add_column("Bonus", justify="right", style="green")
        table.add_row("Number of Characters", "+(n*" + str(nMultLength) + ")", str(nLength), setBonuscolor(sLength))
        table.add_row("Uppercase Letters", "+((len-n)*" + str(nMultAlphaUC) + ")", str(nAlphaUC), setBonuscolor(sAlphaUC))
        table.add_row("Lowercase Letters", "+((len-n)*" + str(nMultAlphaLC) + ")", str(nAlphaLC), setBonuscolor(sAlphaLC))
        table.add_row("Numbers", "+(n*" + str(nMultNumber) + ")", str(nNumber), setBonuscolor(sNumber))
        table.add_row("Symbols", "+(n*" + str(nMultSymbol) + ")", str(nSymbol), setBonuscolor(sSymbol))
        table.add_row("Middle Numbers of Symbols", "+(n*" + str(nMultMidChar) + ")", str(nMidChar), setBonuscolor(sMidChar))
        table.add_row("Requirements", "+(n*" + str(nMultRequirements) + ")", str(nRequirements), setBonuscolor(sRequirements))
        table.add_row("Letters Only", "-n", str(nAlphasOnly), setBonuscolor(sAlphasOnly))
        table.add_row("Numbers Only", "-n", str(nNumbersOnly), setBonuscolor(sNumbersOnly))
        table.add_row("Repeat Characters (Case Insensitive)", "-", str(nRepChar), setBonuscolor(sRepChar))
        table.add_row("Consecutive Uppercase Letters", "-(n*" + str(nMultConsecAlphaUC) + ")", str(nConsecAlphaUC), setBonuscolor(sConsecAlphaUC))
        table.add_row("Consecutive Lowercase Letters", "-(n*" + str(nMultConsecAlphaLC) + ")", str(nConsecAlphaLC), setBonuscolor(sConsecAlphaLC))
        table.add_row("Consecutive Numbers", "-(n*" + str(nMultConsecNumber) + ")", str(nConsecNumber), setBonuscolor(sConsecNumber))
        table.add_row("Sequential Letters (3+)", "-(n*" + str(nMultSeqAlpha) + ")", str(nSeqAlpha), setBonuscolor(sSeqAlpha))
        table.add_row("Sequential Numbers (3+)", "-(n*" + str(nMultSeqNumber) + ")", str(nSeqNumber), setBonuscolor(sSeqNumber))
        table.add_row("Sequential Symbols (3+)", "-(n*" + str(nMultSeqSymbol) + ")", str(nSeqSymbol), setBonuscolor(sSeqSymbol))

        console = Console()
        console.print(table)


if __name__ == '__main__':
    main()
