from fpdf import FPDF
import time

class PDF(FPDF):

    # Author and Title of every page
    def nameTitle(self, title, name):
        self.name = name
        self.title = title

    # Page header
    def header(self):
        # Logo or logo_path (if needed)
        self.image('logo.png', 10, 5, 45)
        # Arial bold 15
        self.set_font('Arial', 'B', 35)
        # Move to the right
        self.cell(150)
        # Title
        self.cell(1, 15, self.title, 0, 2, 'C')
        # Line break
        self.image('footer.png',250,10,45,10)
        self.ln(10)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-10)
        # Arial italic 8
        self.set_font('Arial', 'I', 12)
        # Page number
        actual_date = time.strftime("%d.%b.%Y")
        self.cell(0, 10, (30 * ' ') + self.name + '\t' + (68 * ' ') + 'Page ' + str(self.page_no()) + '/{nb}\t' + (
                    68 * ' ') + actual_date, 0, 0, 'L')

# Method to create the PDF file
def create_pdf(name, title, user_data, illness_data, illness_description, symptoms):
    pdf = PDF()
    pdf.nameTitle(name, title)
    pdf.alias_nb_pages()

    pdf.add_page(orientation='L')
    pdf.set_font('Arial', 'B', 12.0)
    pdf.cell(0, 10, 'User info:', 0, 1,'L')
    pdf.set_font('Arial', '', 12)

    epw = pdf.w - 2 * pdf.l_margin
    col_width = epw / 3
    th = pdf.font_size

    #pdf.ln(2 * th)
    #pdf.ln(0.5)

    for row in user_data:
        for datum in row:
            pdf.cell(col_width, 2 * th, str(datum), border=0)
        pdf.ln(1 * th)

    pdf.ln(5)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Diagnose info:', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)



    epw = pdf.w - 2 * pdf.l_margin
    col_width = epw / 3
    th = pdf.font_size

    #pdf.ln(2 * th)
    #pdf.ln(0.5)
    for row in illness_data:
        for datum in row:
            pdf.cell(col_width, 2 * th, str(datum), border=0)
        pdf.ln(1 * th)
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Illness description:', 0, 1,'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(200, 4, illness_description)


    pdf.add_page(orientation='L')
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Symptoms:', 0, 1,'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(200, 4, symptoms)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Proposed solution:', 0, 1,'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(200, 4, 'Source of information : https://www.orpha.net/consor4.01/www/cgi-bin/OC_Exp.php?lng=EN&Expert=404560')


    pdf.output('informe_pdf.pdf', 'F')

# To test the class and the method.
if __name__ == '__main__':
    user_name = 'User_Name'
    user_surname = 'User_Surname'
    user_phone = '+34 00 000 00 00'
    user_mail = 'user_account@provider.com'
    user_country = 'Spain'
    user_gender = 'User_gender'
    user_age = 'User _age'
    illness_id = 'orpha_ID'
    illness_name = 'Random illness'
    illness_description = 'jdfaljflajfl jadfjdafljdalfjlajfl akdjflakjfoqejkdnalkfldamfa ;lkjlkdafnahladjkfa jkndflkamdfa;k' \
                          'alfkjadsklfakljfkadknakfjkjfklasjdfkjaihfkda fkjakldjfad  shfkjasdkfjakldjfkajdfjadf' \
                          'ajadkfakldfjlakfjdklajdflk aj dfkladjflad jfkadfnauf hafkj dskfja;sldkfja kldjfuijf'
    symptoms = 'kjashdfj ;klasdjf lj fkjdaklfj jfnadsfh uahfka dfjhkaj fhjhfaj h;kjh fakj;aj dnfa;d jkajf ;ja;j uhkadf ' \
               'ha dfljaldjf ;lakjdf ;jkld ;fjkjadjfajf ;lkajdf pieknf kladfm;aljfdsf; a' \
               'a iajdf kla;dfj a;ldjkf a;kf lla;dfj ;adfklj lakjdf; kajdf; adf jk;fa'
    proposed_solution = 'sdlfadklfjakldfjldaskfjklamkdanfjkdanf jdfj kld flkda fjafjlak fjij lkasjd f;jda flk ja;lfj lakj' \
                        'oajdfl aldfjk alkjf ldajf klafj mfajfiaej dafjkljfl j;al jk;lakj dklaj ;j ' \
                        'a  jaljf klafj l;adkj ;lakj ljkfa lja fldj l jlajd ;lfja a' \
                        ' lakjd ;jf lkjal jkf jka;ljd fje kjfafnh;  ajkf jalfj af'
    user_data = [['Name:', user_name, user_surname], ['Contact:', user_phone, user_mail], ['Nationality:', user_country],
                 ['Gender',user_gender],['Age:', user_age]]
    illness_data = [['Illness Name',illness_name],['Illness ID:', illness_id]]

    create_pdf('User Report',user_name, user_data, illness_data, illness_description, symptoms)
