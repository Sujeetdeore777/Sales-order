sheet = workbook.add_worksheet( "GBIprocess " + o.mon )
sheet.write(0, 0, "Report:", bold_format)
sheet.write(0, 1, "Group By item Process")
sheet.write(1, 0, "Period:", bold_format)
sheet.write(1, 1, o.mon)

r = 3
sheet.write(r, 0, "Sr.",bold_format)
sheet.write(r, 1, "cust name", bold_format)

r =4
dd = rdict
_logger.info(dd)
for d in dd:
    _logger.info("************************")
    _logger.info(d)
    sheet.write(r, 0, d ,bold_format)
    sheet.write(r, 1, dd[d] ,bold_format)
    
    r = r + 1