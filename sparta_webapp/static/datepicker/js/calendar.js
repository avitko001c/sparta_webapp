                $('form input[name="birthdate"').datepicker({
                        todayBtn: "linked",
                        calendarWeeks: true,
                        todayHighlight: true,
                        beforeShowDay: function(date){
                                      if (date.getMonth() == (new Date()).getMonth())
                                        switch (date.getDate()){
                                          case 4:
                                            return {
                                              tooltip: 'Example tooltip',
                                              classes: 'active'
                                            };
                                          case 8:
                                            return false;
                                          case 12:
                                            return "green";
                                      }
                                    },
                        toggleActive: true,
                        defaultViewDate: { year: 1977, month: 04, day: 25 }
            });
