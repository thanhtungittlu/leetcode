#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
               ..
              ( '`<
               )(
        ( ----'  '.
        (         ;
         (_______,' 
    ~^~^~^~^~^~^~^~^~^~^~
    Author: thong
    Company: M O B I O
    Date Created: 14/03/2023
"""
from datetime import datetime, timedelta

from .adapter import DataAdapter


class ElasticsearchAdapter(DataAdapter):
    class COMMON(object):
        DATE_TIME_FORMAT = '%Y-%m-%dT%TZ'
        DATE_TIME_FORMAT_2 = '%Y%m%d%H%M%S'
        DATE_TIME_FORMAT_3 = '%Y-%m-%dT%H:%M:%S.%fZ'
        DATE_TIME_FORMAT_4 = '%Y-%m-%dT%H:%M:%S.%f%Z'
        DATE_TIME_FORMAT_5 = '%Y-%m-%d %H:%M:%S'
        DATE_TIME_FORMAT_6 = '%Y-%m-%dT%H:%M:%S.%f'
        DATE_TIME_FORMAT_7 = '%Y-%m-%dT%T.%fZ'
        DATE_TIME_FORMAT_8 = '%Y-%m-%d %H:%M:%S.%f'
        DATE_FORMAT = '%Y%m%d'
        BIRTHDAY_FORMAT = '%d/%m/%Y'

    class TypeDate:
        STRING = "string"
        TIMESTAMP = "timestamp"
        DATE_TIME = "date_time"

    def __init__(self, type_date=TypeDate.TIMESTAMP, format_date=COMMON.DATE_TIME_FORMAT_6):
        self.type_date = type_date
        self.format_date = format_date

    def execute_query(self, query):
        pass

    def build_query(self, policy):
        """
        Between the conditions then and with each other
        Between the statement then and with each other (effect=Deny)
        Between the statement then or with each other (effect=Allow)
        :param policy:
        [{
            "effect": "Allow",
            "condition": [{
                "operator": "StringEquals",
                "field": "user:staff_code",
                "values": ["A123456"],
                "qualifier": "ForAnyValue", // ForAllValues
                "if_exists": True,
                "ignore_case": True,
            }]
        }]
        :return:
        """
        must_policy = []
        should_allow = []  # Allow -> or
        must_deny = []  # Deny -> and
        if policy and isinstance(policy, list):
            for pol in policy:
                conditions = pol.get("condition")
                effect = pol.get("effect")
                if not conditions:
                    if effect == "allow":
                        should_allow.append({
                            "match_all": {}
                        })
                    else:
                        must_deny.append({
                            "must_not": [{
                                "match_all": {}
                            }]
                        })
                else:
                    must = []
                    must_not = []
                    should = []
                    for condition in conditions:
                        must_i, must_not_i, should_i = self.convert_operator_to_query(condition)
                        if must_i:
                            must.extend(must_i)
                        if must_not_i:
                            must.append({
                                "bool": {
                                    "must_not": must_not_i
                                }
                            })
                        if should_i:
                            must.append({
                                "bool": {
                                    "should": should_i
                                }
                            })
                    bool_should = {}
                    if must:
                        bool_should["must"] = must
                    if must_not:
                        bool_should["must_not"] = {
                            "bool": {
                                "must": must_not
                            }
                        }
                    if should:
                        bool_should["should"] = should

                    if effect == "allow":
                        should_allow.append({
                            "bool": bool_should
                        })
                    else:
                        must_deny.append({
                            "bool": {
                                "must_not": {
                                    "bool": bool_should
                                }
                            }

                        })
        if should_allow:
            must_policy.append({
                "bool": {
                    "should": should_allow
                }
            })
        if must_deny:
            must_policy.append({
                "bool": {
                    "must": must_deny
                }
            })

        return {
            "must": must_policy,
            "must_not": [],
            "should": []
        }

    def convert_operator_to_query(self, filter):
        must = []
        must_not = []
        should = []

        operator = filter.get("operator")
        field = filter.get("field")
        values = filter.get("values")
        qualifier = filter.get("qualifier")  # default ForAllValues
        date_format = filter.get("date_format")
        if not field or not operator:
            return must, must_not, should

        field_keys = field.split(":")
        field_key = field_keys[1] if len(field_keys) > 1 else None
        if not field_key:
            return must, must_not, should

        # ----- Check String ----
        if operator in ["StringEquals", "NumericEquals"]:
            if qualifier == "ForAnyValue":
                sh = []
                for value in values:
                    if not value:
                        sh.append({
                            "bool": {
                                "must_not": {
                                    "exists": {
                                        "field": field_key
                                    }
                                }
                            }
                        })
                    else:
                        sh.append({"match": {field_key: value}})
                # sh = [{"match": {field_key: value}} if value else {"match": {field_key: ""}} for value in values]
                should.extend(sh)
            else:
                mu = []
                for value in values:
                    if not value:
                        mu.append({
                            "bool": {
                                "must_not": {
                                    "exists": {
                                        "field": field_key
                                    }
                                }
                            }
                        })
                    else:
                        mu.append({"match": {field_key: value}})
                # mu = [{"match": {field_key: value}} if value else {"match": {field_key: ""}} for value in values]
                must.extend(mu)

        elif operator in ["StringNotEquals", "NumericNotEquals"]:
            if qualifier == "ForAnyValue":
                sh = []
                for value in values:
                    if not value:
                        sh.append({
                            "bool": {
                                "must_not": {
                                    "exists": {
                                        "field": field_key
                                    }
                                }
                            }
                        })
                    else:
                        sh.append({"match": {field_key: value}})
                # sh = [{"match": {field_key: value}} if value else {"match": {field_key: ""}} for value in values]
                must_not.append({
                    "bool": {
                        "should": sh
                    }
                })
            else:
                mu = []
                for value in values:
                    if not value:
                        mu.append({
                            "bool": {
                                "must_not": {
                                    "exists": {
                                        "field": field_key
                                    }
                                }
                            }
                        })
                    else:
                        mu.append({"match": {field_key: value}})
                mu = [{"match": {field_key: value}} if value else {"match": {field_key: ""}} for value in values]
                must_not.extend(mu)
        elif operator == "StringContains":
            if qualifier == "ForAnyValue":
                sh = [{"wildcard": {field_key: "*" + value + "*" if value else "*"}} for value in values]
                should.extend(sh)
            else:
                mu = [{"wildcard": {field_key: "*" + value + "*" if value else "*"}} for value in values]
                must.extend(mu)
        elif operator == "StringNotContains":
            if qualifier == "ForAnyValue":
                sh = [{"wildcard": {field_key: "*" + value + "*" if value else "*"}} for value in values]
                must_not.append({
                    "bool": {
                        "should": sh
                    }
                })
            else:
                mu = [{"wildcard": {field_key: "*" + value + "*" if value else "*"}} for value in values]
                must_not.extend(mu)
        elif operator == "StringEndsWith":
            if qualifier == "ForAnyValue":
                sh = [{"wildcard": {field_key: "*" + value if value else "*"}} for value in values]
                should.extend(sh)
            else:
                mu = [{"wildcard": {field_key: "*" + value if value else '*'}} for value in values]
                must.extend(mu)

        elif operator == "StringStartsWith":
            if qualifier == "ForAnyValue":
                sh = [{"wildcard": {field_key: value + "*" if value else "*"}} for value in values]
                should.extend(sh)
            else:
                mu = [{"wildcard": {field_key: value + "*" if value else "*"}} for value in values]
                must.extend(mu)
        elif operator == "StringMatchesRegex":
            if qualifier == "ForAnyValue":
                sh = [{"regexp": {field_key: value if value else ''}} for value in values]
                should.extend(sh)
            else:
                mu = [{"regexp": {field_key: value if value else ''}} for value in values]
                must.extend(mu)
        elif operator in ["NumericLessThan", "NumericListLessThan"]:
            if qualifier == "ForAnyValue":
                sh = [{"range": {field_key: {"lt": value}}} for value in values]
                should.extend(sh)
            else:
                mu = [{"range": {field_key: {"lt": value}}} for value in values]
                must.extend(mu)
        elif operator in ["NumericLessThanEquals", "NumericListLessThanEquals"]:
            if qualifier == "ForAnyValue":
                sh = [{"range": {field_key: {"lte": value}}} for value in values]
                should.extend(sh)
            else:
                mu = [{"range": {field_key: {"lte": value}}} for value in values]
                must.extend(mu)
        elif operator in ["NumericGreaterThan", "NumericListGreaterThan"]:
            if qualifier == "ForAnyValue":
                sh = [{"range": {field_key: {"gt": value}}} for value in values]
                should.extend(sh)
            else:
                mu = [{"range": {field_key: {"gt": value}}} for value in values]
                must.extend(mu)
        elif operator in ["NumericGreaterThanEquals", "NumericListGreaterThanEquals"]:
            if qualifier == "ForAnyValue":
                sh = [{"range": {field_key: {"gte": value}}} for value in values]
                should.extend(sh)
            else:
                mu = [{"range": {field_key: {"gte": value}}} for value in values]
                must.extend(mu)
        # Tùy data từng bên lưu datetime kiểu gì, Ví dụ Sale lưu theo timestamp thì cần convert ra start_time,
        # end_time trong ngày
        elif operator == "DateEquals":
            for value in values:
                start, end = self.convert_start_time_end_time_by_type(value, date_format)
                if not start or not end:
                    continue
                must.append({"range": {field_key: {"gte": start, "lte": end}}})
        elif operator == "DateNotEquals":
            for value in values:
                start, end = self.convert_start_time_end_time_by_type(value, date_format)
                if not start or not end:
                    continue
                must_not.append({"range": {field_key: {"gte": start, "lte": end}}})
        elif operator == "DateLessThan":
            values = self.convert_list_date_by_type(values, date_format)
            mu = [{"range": {field_key: {"lt": value}}} for value in values]
            must.extend(mu)
        elif operator == "DateLessThanEquals":
            values = self.convert_list_date_by_type(values, date_format)
            mu = [{"range": {field_key: {"lte": value}}} for value in values]
            must.extend(mu)
        elif operator == "DateGreaterThan":
            values = self.convert_list_date_by_type(values, date_format)
            mu = [{"range": {field_key: {"gt": value}}} for value in values]
            must.extend(mu)
        elif operator == "DateGreaterThanEquals":
            values = self.convert_list_date_by_type(values, date_format)
            mu = [{"range": {field_key: {"gte": value}}} for value in values]
            must.extend(mu)

        # Check Day
        elif operator == "DayEquals":
            for value in values:
                start, end = self.convert_day_to_range_by_type(value, date_format)
                if not start or not end:
                    continue
                must.append({"range": {field_key: {"gte": start, "lte": end}}})
        elif operator == "DayNotEquals":
            for value in values:
                start, end = self.convert_day_to_range_by_type(value, date_format)
                if not start or not end:
                    continue
                must_not.append({"range": {field_key: {"gte": start, "lte": end}}})

        elif operator == "DayLessThan":
            values = self.convert_list_start_day_by_type(values, date_format)
            mu = [{"range": {field_key: {"lt": value}}} for value in values]
            must.extend(mu)

        elif operator == "DayLessThanEquals":
            values = self.convert_list_start_day_by_type(values, date_format)
            mu = [{"range": {field_key: {"lte": value}}} for value in values]
            must.extend(mu)
        elif operator == "DayGreaterThan":
            values = self.convert_list_end_day_by_type(values, date_format)
            mu = [{"range": {field_key: {"gt": value}}} for value in values]
            must.extend(mu)
        elif operator == "DayGreaterThanEquals":
            values = self.convert_list_end_day_by_type(values, date_format)
            mu = [{"range": {field_key: {"gte": value}}} for value in values]
            must.extend(mu)

        elif operator == "ListAllIn":
            for value in values:
                if not value:
                    must.append({
                        "bool": {
                            "must_not": {
                                "exists": {
                                    "field": field_key
                                }
                            }
                        }
                    })
                else:
                    must.append({"match": {field_key: value}})
        elif operator == "ListAllNotIn":
            for value in values:
                if not value:
                    must_not.append({
                        "bool": {
                            "must_not": {
                                "exists": {
                                    "field": field_key
                                }
                            }
                        }
                    })
                else:
                    must_not.append({"match": {field_key: value}})
        elif operator == "ListAnyIn":
            if None in values:
                should.append({
                    "bool": {
                        "must_not": {
                            "exists": {
                                "field": field_key
                            }
                        }
                    }
                })
                values.remove(None)
            if values:
                should = [{"terms": {field_key: values}}]
            should.append({"terms": {field_key: values}})
        elif operator == "ListAnyNotIn":
            sh = []
            if None in values:
                sh.append({
                    "bool": {
                        "must_not": {
                            "exists": {
                                "field": field_key
                            }
                        }
                    }
                })
                values.remove(None)
            if values:
                sh = [{"terms": {field_key: values}}]
            must_not.append({"bool": {"should": sh}})
        elif operator == "ListIsIn":
            must.append({"terms": {field_key: values}})
        elif operator == "ListIsNotIn":
            must_not.append({"terms": {field_key: values}})

        elif operator == "ListIsEmpty":
            must.append({
                "bool": {
                    "must_not": [
                        {
                            "exists": {
                                "field": field_key
                            }
                        }
                    ]
                }
            })
        elif operator == "ListIsNotEmpty":
            must.append({"exists": {"field": field_key}})
        elif operator == "ListAnyContains":
            if qualifier == "ForAnyValue":
                sh = [{"wildcard": {field_key: "*" + value + "*" if value else "*"}} for value in values]
                should.extend(sh)
            else:
                mu = [{"wildcard": {field_key: "*" + value + "*" if value else "*"}} for value in values]
                must.extend(mu)
        elif operator == "ListAnyNotContains":
            if qualifier == "ForAnyValue":
                mu = [{"wildcard": {field_key: "*" + value + "*" if value else "*"}} for value in values]
                must_not.extend(mu)
            else:
                sh = [{"wildcard": {field_key: "*" + value + "*" if value else "*"}} for value in values]
                must_not.append({
                    "bool": {
                        "should": sh
                    }
                })
        elif operator == "Exists":
            must.append({
                "exists": {
                    "field": field_key
                }
            })
        elif operator == "NotExists":
            must.append({
                "bool": {
                    "should": [
                        {
                            "bool": {
                                "must_not": [
                                    {
                                        "exists": {
                                            "field": field_key
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "terms": {
                                field_key: []
                            }
                        }
                    ]
                }
            })
        elif operator == "StringNotStartsWith":
            if qualifier == "ForAnyValue":
                sh = [{"wildcard": {field_key: value + "*" if value else "*"}} for value in values]
                must_not.append({
                    "bool": {
                        "should": sh
                    }
                })
            else:
                mu = [{"wildcard": {field_key: value + "*" if value else "*"}} for value in values]
                must_not.extend(mu)
        elif operator == "StringNotEndsWith":
            if qualifier == "ForAnyValue":
                sh = [{"wildcard": {field_key: "*" + value if value else "*"}} for value in values]
                must_not.append({
                    "bool": {
                        "should": sh
                    }
                })
            else:
                mu = [{"wildcard": {field_key: "*" + value if value else "*"}} for value in values]
                must_not.extend(mu)

        return must, must_not, should

    @staticmethod
    def convert_date_to_range_timestamp(date, date_format):
        """
        :param date:
        :param date_format:
        :return:
        """
        try:
            date_input = datetime.strptime(date, date_format)
            end_time = date_input.replace(second=59).timestamp()
            start_time = end_time - (60)
            return start_time, end_time
        except Exception:
            return None, None

    @staticmethod
    def convert_list_date_to_timestamp(lst_date, date_format):
        """
        :param lst_date:
        :param date_format:
        :return:
        """
        values = []
        for d in lst_date:
            try:
                value = datetime.strptime(d, date_format).timestamp()
                values.append(value)
            except Exception:
                pass
        return values

    @staticmethod
    def convert_day_to_range_timestamp(date, date_format):
        """
        :param date:
        :param date_format:
        :return:
        """
        try:
            date_input = datetime.strptime(date, date_format)
            end_time = date_input.replace(hour=17, minute=0, second=0).timestamp()
            start_time = end_time - (24 * 3600)
            return start_time, end_time
        except Exception:
            return None, None

    @staticmethod
    def convert_list_end_day_to_timestamp(lst_date, date_format):
        """
        :param lst_date:
        :param date_format:
        :return:
        """
        values = []
        for d in lst_date:
            try:
                value = datetime.strptime(d, date_format).replace(hour=17, minute=59, second=59).timestamp()
                values.append(value)
            except Exception:
                pass
        return values

    @staticmethod
    def convert_list_start_day_to_timestamp(lst_date, date_format):
        """
        :param lst_date:
        :return:
        """
        values = []
        for d in lst_date:
            try:
                value = datetime.strptime(d, date_format).replace(hour=17, minute=59, second=59).timestamp() - (
                        24 * 3600)
                values.append(value)
            except Exception:
                pass
        return values

    def convert_format_day_to_range(self, date, date_format):
        """
        :param date:
        :param date_format:
        :return:
        """
        try:
            start_date = datetime.strptime(date, date_format)
            end_date = datetime(year=start_date.year, month=start_date.month, day=start_date.day, hour=start_date.hour,
                                minute=start_date.minute) + timedelta(seconds=59)
            start_time = start_date.strftime(self.format_date)[:-3] + 'Z'
            end_time = end_date.strftime(self.format_date)[:-3] + 'Z'
            return start_time, end_time
        except Exception:
            return None, None

    def convert_format_list_day(self, lst_date, date_format):
        """
        :param lst_date:
        :return:
        """
        values = []
        for d in lst_date:
            try:
                value = datetime.strptime(d, date_format).strftime(self.format_date)[
                        :-3] + 'Z'
                values.append(value)
            except Exception:
                pass
        return values

    def convert_start_time_end_time_by_type(self, date, date_format):
        if self.type_date == self.TypeDate.TIMESTAMP:
            start, end = self.convert_date_to_range_timestamp(date, date_format)
        elif self.type_date == self.TypeDate.DATE_TIME:
            start = datetime.strptime(date, date_format)
            end = datetime(year=start.year, month=start.month, day=start.day, hour=start.hour,
                           minute=start.minute) + timedelta(seconds=59)
        else:
            start, end = self.convert_format_day_to_range(date, date_format)
        return start, end

    def convert_list_date_by_type(self, lst_date, date_format):
        if self.type_date == self.TypeDate.TIMESTAMP:
            values = self.convert_list_date_to_timestamp(lst_date, date_format)
        elif self.type_date == self.TypeDate.DATE_TIME:
            values = []
            for d in lst_date:
                values.append(datetime.strptime(d, date_format))
        else:
            values = self.convert_format_list_day(lst_date, date_format)
        return values

    def convert_day_to_range_by_type(self, date, date_format):
        if self.type_date == self.TypeDate.TIMESTAMP:
            start, end = self.convert_day_to_range_timestamp(date, date_format)
        elif self.type_date == self.TypeDate.DATE_TIME:
            start = datetime.strptime(date, date_format)
            end = datetime(year=start.year, month=start.month, day=start.day, hour=start.hour,
                           minute=start.minute) + timedelta(seconds=59)
        else:
            start, end = self.convert_format_day_to_range(date, date_format)
        return start, end

    def convert_list_start_day_by_type(self, lst_date, date_format):
        if self.type_date == self.TypeDate.TIMESTAMP:
            values = self.convert_list_start_day_to_timestamp(lst_date, date_format)
        elif self.type_date == self.TypeDate.DATE_TIME:
            values = []
            for d in lst_date:
                values.append(datetime.strptime(d, date_format))
        else:
            values = self.convert_format_list_day(lst_date, date_format)
        return values

    def convert_list_end_day_by_type(self, lst_date, date_format):
        if self.type_date == self.TypeDate.TIMESTAMP:
            values = self.convert_list_end_day_to_timestamp(lst_date, date_format)
        elif self.type_date == self.TypeDate.DATE_TIME:
            values = []
            for d in lst_date:
                values.append(datetime.strptime(d, date_format))
        else:
            values = self.convert_format_list_day(lst_date, date_format)
        return values
