
from . import api
from .. import db

from ..helpers import get_existing_order_from_request, post_process_order
from ..socketio import emit_update
from ..models import OrderItem


@api.route('/void_line', methods=['POST'])
def void_line():
    """
    Void lines from existing order
    :return:
    """
    existing_order, request_data = get_existing_order_from_request()
    print("IDD")
    print(request_data.get('item_code'))
    item = [item for item in existing_order.items if item.item_code == request_data.get('item_code')][0]
    print(item)
    item.is_voided = True

    if request_data.get('amend'):
        new_qty = request_data.get('qty')

        item_clone = OrderItem.clone(item)
        item_clone.qty = new_qty

        if item.qty <= new_qty:
            raise Exception('Qty should be less than old qty.')

        existing_order.items.append(item_clone)
        existing_order.append_remarks(
            'AMEND QTY {} to {}'.format(item_clone.item_name, item_clone.qty)
        )

    else:
        existing_order.append_remarks(
            'VOID {}'.format(item.item_name)
        )

    db.session.add(existing_order)
    db.session.add(item)
    db.session.commit()

    emit_update(existing_order, 'void')

    return post_process_order(existing_order), 200

