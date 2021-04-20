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

"""
sample history
        {
            'id': 1,
            'function': "f(a) = m(1,2)+ d(3)
            'solution': "bcd' + bc'd + a'b'",
            "pi_chart": "",
            "reduced_pi_chart": "",
            'time_created': "2021-04-17:17:00:00"
        }
"""
history_data = []

def get_history_data():
    return sorted(history_data, key=lambda x: datetime.strptime(x["time_created"], "%Y-%m-%d:%H:%M:%S"), reverse=True)