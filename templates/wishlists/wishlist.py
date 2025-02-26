{% extends "base/base2.html" %}
{% block title %}Wishlist{% endblock title %}

{% block section %}
<div class="bg0 p-t-75 p-b-85">
    <div class="container">
        <div class="row">
            <div class="col-lg-10 col-xl-7 m-lr-auto m-b-50">
                <div class="m-l-25 m-r--38 m-lr-0-xl">
                    <h4 class="mtext-109 cl2 p-b-30">
                        Your Wishlist
                    </h4>

                    <!-- Wishlist Table -->
                    <div class="wrap-table-shopping-cart">
                        <table class="table-shopping-cart">
                            <tr class="table_head">
                                <th class="column-1">Product</th>
                                <th class="column-2"></th>
                                <th class="column-3">Price</th>
                                <th class="column-4">Action</th>
                            </tr>

                            {% for item in wishlist.items.all %}
                            <tr class="table_row">
                                <td class="column-1">
                                    <div class="how-itemcart1">
                                        <img src="{{ item.product.image.url }}" alt="IMG">
                                    </div>
                                </td>
                                <td class="column-2">{{ item.product.name }}</td>
                                <td class="column-3">$ {{ item.product.price }}</td>
                                <td class="column-4">
                                    <div class="flex-w">
                                        <form action="{% url 'move_to_cart' item.id %}" method="POST" class="m-r-10">
                                            {% csrf_token %}
                                            <button type="submit" class="flex-c-m stext-101 cl2 size-115 bg8 bor13 hov-btn3 p-lr-15 trans-04 pointer">
                                                Move to Cart
                                            </button>
                                        </form>
                                        <form action="{% url 'remove_from_wishlist' item.id %}" method="POST">
                                            {% csrf_token %}
                                            <button type="submit" class="flex-c-m stext-101 cl2 size-115 bg8 bor13 hov-btn3 p-lr-15 trans-04 pointer">
                                                Remove
                                            </button>
                                        </form>
                                    </div>
                                </td>
                            </tr>
                            {% empty %}
                            <tr class="table_row">
                                <td colspan="4" class="text-center p-t-30 p-b-30">
                                    <p class="stext-110 cl6">Your wishlist is empty.</p>
                                </td>
                            </tr>
                            {% endfor %}
                        </table>
                    </div>
                </div>
            </div>

            <div class="col-sm-10 col-lg-7 col-xl-5 m-lr-auto m-b-50">
                <div class="bor10 p-lr-40 p-t-30 p-b-40 m-l-63 m-r-40 m-lr-0-xl p-lr-15-sm">
                    <h4 class="mtext-109 cl2 p-b-30">
                        Wishlist Summary
                    </h4>

                    <div class="flex-w flex-t bor12 p-b-13">
                        <div class="size-208">
                            <span class="stext-110 cl2">
                                Total Items:
                            </span>
                        </div>

                        <div class="size-209">
                            <span class="mtext-110 cl2">
                                {{ wishlist.items.count }}
                            </span>
                        </div>
                    </div>

                    <div class="flex-w flex-t p-t-27 p-b-33">
                        <div class="size-208">
                            <span class="mtext-101 cl2">
                                Total Price:
                            </span>
                        </div>

                        <div class="size-209 p-t-1">
                            <span class="mtext-110 cl2">
                                ${{ wishlist.get_total_price }}
                            </span>
                        </div>
                    </div>

                    <!-- Continue Shopping Button -->
                    <div class="text-center">
                        <a href="{% url 'home' %}" class="flex-c-m stext-101 cl0 size-116 bg3 bor14 hov-btn3 p-lr-15 trans-04 pointer">
                            Continue Shopping
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock section %}