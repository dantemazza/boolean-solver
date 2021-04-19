from datetime import datetime

solution_html = """
  <h1>
    Prime Implicant Chart
  </h1>
  <p>
    {}
  </p>
  <h1>
    Reduced Prime Implicant Chart
  </h1>
  <p>
    {}
  </p>
  <h1>
    Final Expression
  </h1>
  <h5>
    <b>{}</b>
  </h5>
  """

def history():
    history = [
        {
            'id': 1,
            'minterms': [0, 1, 2, 5, 6, 13, 14, 15],
            'maxterms': [4, 7, 8, 9, 10, 12],
            "dont_cares": [3, 11],
            'solution': "bcd' + bc'd + a'b'",
            "pi_chart": "",
            "reduced_pi_chart": "",
            'time_created': "2021-04-17:17:00:00"
        },
        {
            'id': 2,
            'minterms': [0, 1, 2, 5, 6, 13, 14, 15],
            'maxterms': [4, 7, 8, 9, 10, 12],
            "dont_cares": [3, 11],
            'solution': "bcd' + bc'd + a'b'",
            "pi_chart": "",
            "reduced_pi_chart": "",
            'time_created': "2021-04-17:18:00:00"

        },
        {
            'id': 3,
            'minterms': [0, 1, 2, 5, 6, 13, 14, 15],
            'maxterms': [4, 7, 8, 9, 10, 12],
            "dont_cares": [3, 11],
            'solution': "bcd' + bc'd + a'b'",
            "pi_chart": "",
            "reduced_pi_chart": "",
            'time_created': "2021-04-17:16:00:00"
        }
    ]

    return sorted(history, key=lambda x: datetime.strptime(x["time_created"], "%Y-%m-%d:%H:%M:%S"), reverse=True)