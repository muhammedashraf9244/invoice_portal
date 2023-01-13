# -*- coding: utf-8 -*-
from io import BytesIO

from PyPDF2 import PdfFileReader

from odoo import http
from odoo.http import request, content_disposition
from odoo.tools.pdf import PdfFileWriter


class InvoicePortal(http.Controller):
    @http.route('/invoice_portal/html', type="http", auth='user', website=True)
    def get_invoice_portal_html(self, **kw):
        user = request.env.user
        if user.partner_id:
            # get invoices
            sql = f"""select id from account_move as e 
            where partner_id = {user.partner_id.id}
            ORDER BY e.invoice_date DESC
            LIMIT 200;"""
            request.env.cr.execute(sql)
            raw_data = request.env.cr.dictfetchall()  # [{'id':15}, {'id': 16}]
            docids = [e.get('id') for e in raw_data]  # [15,16]
            report_name = 'invoice_portal.report_invoice_portal_template'
            report = request.env['ir.actions.report'].sudo()._get_report_from_name(report_name)
            context = dict(request.env.context)
            html = report.with_context(context).sudo()._render_qweb_html(docids)[0]
            return request.make_response(html)
        else:
            return request.not_found()

    # @http.route('/invoice_portal/pdf', type="http", auth='user', website=True)
    # def get_invoice_portal_pdf(self, **kw):
    #     user = request.env.user
    #     if user.partner_id:
    #         # get invoices
    #         sql = f"""select id from account_move as e
    #             where partner_id = {user.partner_id.id}
    #             ORDER BY e.invoice_date DESC
    #             LIMIT 200;"""
    #         request.env.cr.execute(sql)
    #         raw_data = request.env.cr.dictfetchall()  # [{'id':15}, {'id': 16}]
    #         docids = [e.get('id') for e in raw_data]  # [15,16]
    #         report_name = 'invoice_portal.report_invoice_portal_template'
    #         report = request.env['ir.actions.report'].sudo()._get_report_from_name(report_name)
    #         context = dict(request.env.context)
    #         pdf = report.with_context(context)._render_qweb_pdf(docids)[0]
    #         pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
    #         return request.make_response(pdf, headers=pdfhttpheaders)
    #     else:
    #         return request.not_found()
    @http.route('/invoice_portal/pdf', type="http", auth='user', website=True)
    def get_invoice_portal_pdf(self, **kw):
        user = request.env.user
        if user.partner_id:
            # get invoices
            sql = f"""select id from account_move as e 
                       where partner_id = {user.partner_id.id}
                       ORDER BY e.invoice_date DESC
                       LIMIT 400;"""
            request.env.cr.execute(sql)
            raw_data = request.env.cr.dictfetchall()  # [{'id':15}, {'id': 16}]
            docids = [e.get('id') for e in raw_data]  # [15,16]
            report_name = 'invoice_portal.report_invoice_portal_template'
            report = request.env['ir.actions.report'].sudo()._get_report_from_name(report_name)
            # context = dict(request.env.context)
            # pdf = report.with_context(context)._render_qweb_pdf(docids)[0]
            # pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
            # return request.make_response(pdf, headers=pdfhttpheaders)
            pdf_writer = PdfFileWriter()
            for move_id in docids:
                pdf_content, _ = report._render_qweb_pdf(move_id)
                reader = PdfFileReader(BytesIO(pdf_content), strict=False, overwriteWarnings=False)
                for page in range(reader.getNumPages()):
                    pdf_writer.addPage(reader.getPage(page))

            _buffer = BytesIO()
            pdf_writer.write(_buffer)
            merged_pdf = _buffer.getvalue()
            _buffer.close()
            file_name = "Invoices"
            pdfhttpheaders = [
                ('Content-Type', 'application/pdf'),
                ('Content-Length', len(merged_pdf)),
                ('Content-Disposition', content_disposition(file_name + '.pdf'))
            ]
            return request.make_response(merged_pdf, headers=pdfhttpheaders)
        else:
            return request.not_found()
