sheet = workbook.add_worksheet( "GBIprocess " + o.mon )
sheet.write(0, 0, "Report:", bold_format)
sheet.write(0, 1, "Group By item Process")
sheet.write(1, 0, "Period:", bold_format)
sheet.write(1, 1, o.mon)

rdict = self.reportcalc()
_logger.info(rdict)

sheet.write(3, 0, "Item", bold_format)
sheet.write(3, 1, "total_mfg_qty", bold_format)
sheet.write(3, 2, "total_disp_qty", bold_format)
sheet.write(3, 3, "open_order_qty", bold_format)

r =4
dd = rdict
_logger.info(dd)
for d in dd:
    _logger.info("************************")
    _logger.info(d)
    sheet.write(r, 0, d )
    sheet.write(r, 1, dd[d]['total_mfg_qty'] )
    sheet.write(r, 2, dd[d]['total_disp_qty'] )
    sheet.write(r, 3, dd[d]['open_order_qty'] )
    
    r = r + 1