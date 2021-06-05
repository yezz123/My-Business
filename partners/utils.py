from partners.models import Partner


def generate_id(string):
    if len(string.split()) == 3:
        partner_id = "".join(word[0] for word in string.split()).upper()
    else:
        string = "".join(letter for letter in string if letter.isalnum()).upper()
        partner_id = string[0]
        partner_id += string[int(len(string) / 2)]
        partner_id += string[-1]
    if Partner.objects.filter(partner_id=partner_id).count() > 0:
        if len(string.split()) == 3:
            string = "".join(letter for letter in string if letter.isalnum()).upper()
            partner_id = string[0]
            partner_id += string[int(len(string) / 2)]
            partner_id += string[-1]
            if Partner.objects.filter(partner_id=partner_id).count() == 0:
                return partner_id
        return generate_id(string[:-1])
    return partner_id
