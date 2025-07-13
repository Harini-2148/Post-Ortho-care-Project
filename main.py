import csv
import re

# Sample JSON data
sample_json = {
    "user": {
        "id": 101,
        "name": {
            "first": "John",
            "last": "Doe"
        },
        "contact": {
            "emails": ["john.doe@example.com", "j.doe@workmail.com"],
            "phone": "1234567890"
        }
    },
    "orders": [
        {
            "order_id": "A001",
            "date": "2025-06-20",
            "items": [
                {"product": "Laptop", "price": 1200},
                {"product": "Mouse", "price": 25}
            ]
        },
        {
            "order_id": "A002",
            "date": "2025-06-21",
            "items": [
                {"product": "Keyboard", "price": 45}
            ]
        }
    ],
    "location": {
        "city": "New York",
        "zipcode": "10001"
    }
}

# Mapping keys
mapping_dict = {
    "user.id": "User ID",
    "user.name.first": "First Name",
    "user.name.last": "Last Name",
    "user.contact.phone": "Phone Number",
    "location.city": "City",
    "location.zipcode": "Zip Code",
    "orders[*].order_id": "Order ID",
    "orders[*].date": "Order Date",
    "orders[*].items[*].product": "Product Name",
    "orders[*].items[*].price": "Product Price"
}

# Converter class
class JSONToCSVConverter:
    def __init__(self, mapping):
        self.mapping = mapping

    def flatten(self, obj, parent_key=''):
        items = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_key = f"{parent_key}.{k}" if parent_key else k
                items.extend(self.flatten(v, new_key).items())
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                new_key = f"{parent_key}[{i}]"
                items.extend(self.flatten(v, new_key).items())
        else:
            items.append((parent_key, obj))
        return dict(items)

    def match_and_rename_key(self, key):
        for pattern, name in self.mapping.items():
            pattern_regex = '^' + re.escape(pattern).replace(r'\[\*\]', r'\[\d+\]') + '$'
            if re.fullmatch(pattern_regex, key):
                return name
        return key

    def apply_mapping(self, flat_dict):
        return {self.match_and_rename_key(k): v for k, v in flat_dict.items()}

    def build_rows(self, data):
        user_info = self.flatten(data.get("user", {}))
        location_info = self.flatten(data.get("location", {}))
        base_info = {**user_info, **location_info}

        rows = []
        for order in data.get("orders", []):
            order_info = self.flatten(order)
            for item in order.get("items", []):
                item_info = self.flatten(item)
                combined = {**base_info, **order_info, **item_info}
                row = self.apply_mapping(combined)
                rows.append(row)
        return rows

    def convert_to_csv(self, data, output_path):
        rows = self.build_rows(data)
        if not rows:
            print("❌ No data to write.")
            return
        # Write to CSV
        with open(output_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"✅ CSV conversion successful. File saved as: {output_path}")

# Run it
if __name__ == "__main__":
    converter = JSONToCSVConverter(mapping_dict)
    converter.convert_to_csv(sample_json, "output.csv")
