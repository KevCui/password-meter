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

    nTmpAlphaUC = nTmpAlphaLC = nTmpNumber = ""
    sAlphas = "abcdefghijklmnopqrstuvwxyz"
    sNumerics = "01234567890"
    sSymbols = ")!@#$%^&*()"
    nMinPwdLen = 8
    nMinReqChars = 4
    dictRule = {
        "length": {"count": 0, "mult": 4, "score": 0, "text": "Number of Characters", "rate": "+(n*4)"},
        "alphaUC": {"count": 0, "mult": 2, "score": 0, "text": "Uppercase Letters", "rate": "+((len-n)*2)"},
        "alphaLC": {"count": 0, "mult": 2, "score": 0, "text": "Lowercase Letters", "rate": "+((len-n)*2)"},
        "number": {"count": 0, "mult": 4, "score": 0, "text": "Numbers", "rate": "+(n*4)"},
        "symbol": {"count": 0, "mult": 6, "score": 0, "text": "Symbols", "rate": "+(n*6)"},
        "midChar": {"count": 0, "mult": 2, "score": 0, "text": "Middle Numbers of Symbols", "rate": "+(n*2)"},
        "requirements": {"count": 0, "mult": 0, "score": 0, "text": "Requirements", "rate": "+(n*2)"},
        "alphasOnly": {"count": 0, "mult": -1, "score": 0, "text": "Letters Only", "rate": "-n"},
        "numbersOnly": {"count": 0, "mult": -1, "score": 0, "text": "Numbers Only", "rate": "-n"},
        "repChar": {"count": 0, "mult": -1, "score": 0, "text": "Repeat Characters", "rate": "-?"},
        "consecAlphaUC": {"count": 0, "mult": -2, "score": 0, "text": "Consecutive Uppercase Letters", "rate": "-(n*2)"},
        "consecAlphaLC": {"count": 0, "mult": -2, "score": 0, "text": "Consecutive Lowercase Letters", "rate": "-(n*2)"},
        "consecNumber": {"count": 0, "mult": -2, "score": 0, "text": "Consecutive Numbers", "rate": "-(n*2)"},
        "seqAlpha": {"count": 0, "mult": -3, "score": 0, "text": "Sequential Letters (3+)", "rate": "-(n*3)"},
        "seqNumber": {"count": 0, "mult": -3, "score": 0, "text": "Sequential Numbers (3+)", "rate": "-(n*3)"},
        "seqSymbol": {"count": 0, "mult": -3, "score": 0, "text": "Sequential Symbols (3+)", "rate": "-(n*3)"}
    }
    if args.password:
        pwd = args.password[0]
    else:
        try:
            pwd = getpass()
        except KeyboardInterrupt:
            sys.exit(1)
    dictRule["length"]["count"] = len(pwd)
    arrPwd = list(pwd)
    arrPwdLen = len(arrPwd)
    score = 0

    # Check Uppercase, Lowercase, Numeric and Symbol
    nRepInc = 0
    for a in range(0, arrPwdLen):
        if re.match(r'[A-Z]', arrPwd[a]):
            if nTmpAlphaUC != "":
                if (nTmpAlphaUC + 1) == a:
                    dictRule["consecAlphaUC"]["count"] += 1
            nTmpAlphaUC = a
            dictRule["alphaUC"]["count"] += 1
        elif re.match(r'[a-z]', arrPwd[a]):
            if nTmpAlphaLC != "":
                if (nTmpAlphaLC + 1) == a:
                    dictRule["consecAlphaLC"]["count"] += 1
            nTmpAlphaLC = a
            dictRule["alphaLC"]["count"] += 1
        elif re.match(r'[0-9]', arrPwd[a]):
            if a > 0 and a < (arrPwdLen - 1):
                dictRule["midChar"]["count"] += 1
            if nTmpNumber != "":
                if (nTmpNumber + 1) == a:
                    dictRule["consecNumber"]["count"] += 1
            nTmpNumber = a
            dictRule["number"]["count"] += 1
        elif re.match(r'[^a-zA-Z0-9_]', arrPwd[a]):
            if a > 0 and a < (arrPwdLen - 1):
                dictRule["midChar"]["count"] += 1
            dictRule["symbol"]["count"] += 1

        # Check for repeat characters
        bCharExists = False
        for b in range(0, arrPwdLen):
            if arrPwd[a] == arrPwd[b] and a != b:
                bCharExists = True
                nRepInc += abs(arrPwdLen/(b-a))

        if bCharExists:
            dictRule["repChar"]["count"] += 1
            nUnqChar = arrPwdLen - dictRule["repChar"]["count"]
            nRepInc = math.ceil(nRepInc/nUnqChar) if nUnqChar else math.ceil(nRepInc)
    dictRule["repChar"]["score"] = nRepInc * dictRule["repChar"]["mult"]

    if dictRule["alphaLC"]["count"] > 0 and dictRule["alphaLC"]["count"] < dictRule["length"]["count"]:
        dictRule["alphaLC"]["score"] = (dictRule["length"]["count"] - dictRule["alphaLC"]["count"]) * dictRule["alphaLC"]["mult"]
    if dictRule["alphaUC"]["count"] > 0 and dictRule["alphaUC"]["count"] < dictRule["length"]["count"]:
        dictRule["alphaUC"]["score"] = (dictRule["length"]["count"] - dictRule["alphaUC"]["count"]) * dictRule["alphaUC"]["mult"]

    # Check for sequential alpha string patterns (forward and reverse)
    for s in range(0, 24):
        sFwd = sAlphas[s:s+3]
        sRev = sFwd[::-1]
        if pwd.lower().find(sFwd) != -1 or pwd.lower().find(sRev) != -1:
            dictRule["seqAlpha"]["count"] += 1

    # Check for sequential numeric string patterns (forward and reverse)
    for s in range(0, 9):
        sFwd = sNumerics[s:s+3]
        sRev = sFwd[::-1]
        if pwd.lower().find(sFwd) != -1 or pwd.lower().find(sRev) != -1:
            dictRule["seqNumber"]["count"] += 1

    # Check for sequential symbol string patterns (forward and reverse)
    for s in range(0, 9):
        sFwd = sSymbols[s:s+3]
        sRev = sFwd[::-1]
        if pwd.lower().find(sFwd) != -1 or pwd.lower().find(sRev) != -1:
            dictRule["seqSymbol"]["count"] += 1

    # Point deductions
    if max(dictRule["alphaLC"]["count"], dictRule["alphaUC"]["count"]) > 0 and max(dictRule["symbol"]["count"], dictRule["number"]["count"]) == 0:
        dictRule["alphasOnly"]["count"] = dictRule["length"]["count"]

    if max(dictRule["alphaLC"]["count"], dictRule["alphaUC"]["count"], dictRule["symbol"]["count"]) == 0 and dictRule["number"]["count"] > 0:
        dictRule["numbersOnly"]["count"] = dictRule["length"]["count"]

    # Determine if mandatory requirements have been met
    arrChars = ["alphaUC", "alphaLC", "number", "symbol"]
    for c in arrChars:
        if dictRule[c]["count"] > 0:
            dictRule["requirements"]["count"] += 1

    if dictRule["length"]["count"] >= nMinPwdLen:
        dictRule["requirements"]["count"] += 1
        if dictRule["requirements"]["count"] >= nMinReqChars:
            dictRule["requirements"]["mult"] = 2

    for k in dictRule.keys():
        if dictRule[k]["count"] > 0:
            if dictRule[k]["score"] == 0:
                dictRule[k]["score"] = dictRule[k]["count"] * dictRule[k]["mult"]
            score += dictRule[k]["score"]

    fScore, fComplexity = calcResult(score)
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
        for k in dictRule.keys():
            table.add_row(dictRule[k]["text"], dictRule[k]["rate"], str(dictRule[k]["count"]), setBonuscolor(dictRule[k]['score']))

        console = Console()
        console.print(table)


if __name__ == '__main__':
    main()
