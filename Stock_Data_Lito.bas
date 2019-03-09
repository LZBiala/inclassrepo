Attribute VB_Name = "Stock_Data_Lito"
Sub Stock_Data()

    For Each ws In Worksheets
    ws.Activate
    
    
    Dim WorksheetName As String
    WorksheetName = ws.Name
     
    LastRow = ws.Cells(Rows.Count, 1).End(xlUp).Row
     
    Dim S_Data As String
    Dim S_Total As Double
    S_Total = 0
     
    Dim Summary_Table_Row As Integer
    Summary_Table_Row = 2
    
    ws.Cells(1, 8).Value = "Ticker"
    ws.Cells(1, 9).Value = "Total Stock Volume"
     
        For i = 2 To LastRow
         
        If ws.Cells(i + 1, 1).Value <> ws.Cells(i, 1).Value Then
            
            S_Data = Cells(i, 1).Value
            S_Total = S_Total + Cells(i, 7).Value
                
            Range("H" & Summary_Table_Row).Value = S_Data
            Range("I" & Summary_Table_Row).Value = S_Total
                
            Summary_Table_Row = Summary_Table_Row + 1
                
            S_Total = 0
                
            Else
            
            S_Total = S_Total + Cells(i, 7).Value
            
            End If
            
        Next i
        
    Next ws
    
    
End Sub
