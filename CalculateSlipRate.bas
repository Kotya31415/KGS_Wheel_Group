Attribute VB_Name = "Module1"



Sub CalculateSlipRate1()

    Dim ws As Worksheet
    Dim lastRow As Long
    Dim finalDeg As Double
    Dim xActual As Double
    Dim xTheoretical As Double
    Dim slipRate As Double

    Set ws = ActiveSheet

    ' C列の最終データ行を取得
    lastRow = ws.Cells(ws.Rows.Count, "C").End(xlUp).Row

    ' C列の最終角度取得
    finalDeg = ws.Cells(lastRow, "C").Value

    ' F2に入力された実測移動距離
    xActual = ws.Range("F2").Value

    ' 理論移動距離
    xTheoretical = Abs(finalDeg) / 360# * 6# * WorksheetFunction.Pi()

    ' スリップ率
    If xTheoretical <> 0 Then
        slipRate = 1 - (xActual / xTheoretical)
    Else
        MsgBox "理論移動距離が0です。", vbExclamation
        Exit Sub
    End If

    ' 見出し
    ws.Range("G1").Value = "X_theoretical"
    ws.Range("H1").Value = "Slip_Rate"

    ' 結果出力
    ws.Range("G2").Value = xTheoretical
    ws.Range("H2").Value = slipRate

    ' 書式設定
    ws.Range("G2").NumberFormat = "0.000"
    ws.Range("H2").NumberFormat = "0.00%"

    MsgBox "計算完了", vbInformation

End Sub
