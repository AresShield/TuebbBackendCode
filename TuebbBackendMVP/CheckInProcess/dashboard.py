import datetime

#string representatation of datetime = "27.08.2021 14:22"
format_string = "%d.%m.%Y %H:%M"

def get_dashboard_data(venue, params):
    start = datetime.datetime.strptime(params.get("start"), format_string)
    end = datetime.datetime.strptime(params.get("end"), format_string)
    tickets = venue.tickets.filter(created__range=(start, end)).filter(paid=True)
    total_sold = len(tickets)
    ticket_revenue = total_sold * venue.entry_fee
    age = 0
    females, males, nonbinary, other = 0,0,0,0
    for t in tickets:
        user = t.owner.consumer_account.all()[0]
        match user.gender:
            case "Female":
                females += 1
            case "Male":
                males += 1
            case "Non-binary":
                nonbinary += 1
            case "Other":
                other += 1
        age += user.age

    females /= total_sold
    males /= total_sold
    nonbinary /= total_sold
    other /= total_sold
    age /= total_sold

    return {
        "total_sold": total_sold,
        "ticket_revenue": ticket_revenue,
        "avg_age": age,
        "female_perc": females,
        "male_perc": males,
        "non_binary_perc": nonbinary,
        "other_perc": other
    }
