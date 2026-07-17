from __future__ import annotations

from dataclasses import dataclass

from django.urls import reverse

from catalog.models import Brand, Category, Product


@dataclass(frozen=True)
class SitemapNode:
    title: str
    url: str
    depth: int
    has_children: bool = False


def _format_sitemap_title(title: str, depth: int) -> str:
    title = (title or '').strip()
    if not title:
        return title
    if depth == 2:
        return title.upper()
    if depth >= 3:
        return title[0].upper() + title[1:].lower()
    return title


def _node(title: str, url: str, depth: int) -> SitemapNode:
    return SitemapNode(
        title=_format_sitemap_title(title, depth),
        url=url,
        depth=depth,
    )


def _annotate_has_children(nodes: list[SitemapNode]) -> list[SitemapNode]:
    annotated: list[SitemapNode] = []
    for index, node in enumerate(nodes):
        has_children = (
            index + 1 < len(nodes)
            and nodes[index + 1].depth > node.depth
        )
        annotated.append(
            SitemapNode(
                title=node.title,
                url=node.url,
                depth=node.depth,
                has_children=has_children,
            )
        )
    return annotated


def _brand_certificate_ids() -> set[int]:
    return set(
        Brand.visible.filter(product__modelfile__isnull=False)
        .distinct()
        .values_list('id', flat=True)
    )


def _append_category_branch(
    nodes: list[SitemapNode],
    category: Category,
    depth: int,
    children_by_parent: dict[int, list[Category]],
    products_by_category: dict[int, list[Product]],
) -> None:
    nodes.append(
        _node(
            category.name or '',
            category.get_absolute_url(),
            depth,
        )
    )

    for child in children_by_parent.get(category.id, []):
        _append_category_branch(
            nodes,
            child,
            depth + 1,
            children_by_parent,
            products_by_category,
        )

    for product in products_by_category.get(category.id, []):
        if not product.brand_id or not product.slug:
            continue
        nodes.append(
            _node(
                product.name or '',
                product.get_absolute_url(),
                depth + 1,
            )
        )


def build_sitemap_nodes() -> list[SitemapNode]:
    nodes: list[SitemapNode] = [
        SitemapNode(title='Главная', url=reverse('home'), depth=0),
        SitemapNode(title='Условия работы', url=reverse('work'), depth=1),
        SitemapNode(title='Каталог', url=f"{reverse('home')}#catalog", depth=1),
    ]

    brands = list(Brand.visible.order_by('place', 'name'))
    categories = list(
        Category.visible.select_related('brand').prefetch_related('parents').order_by('place', 'name')
    )
    products = list(
        Product.visible.select_related('brand').prefetch_related('parents').order_by('place', 'name')
    )

    children_by_parent: dict[int, list[Category]] = {}
    root_categories_by_brand: dict[int, list[Category]] = {}

    for category in categories:
        parent_ids = [parent.id for parent in category.parents.all()]
        if parent_ids:
            for parent_id in parent_ids:
                children_by_parent.setdefault(parent_id, []).append(category)
        elif category.brand_id:
            root_categories_by_brand.setdefault(category.brand_id, []).append(category)

    for child_list in children_by_parent.values():
        child_list.sort(key=lambda item: (item.place or 0, item.name or ''))
    for root_list in root_categories_by_brand.values():
        root_list.sort(key=lambda item: (item.place or 0, item.name or ''))

    products_by_category: dict[int, list[Product]] = {}
    direct_products_by_brand: dict[int, list[Product]] = {}

    for product in products:
        if not product.brand_id or not product.slug:
            continue
        parent_categories = list(product.parents.all())
        if parent_categories:
            for parent in parent_categories:
                products_by_category.setdefault(parent.id, []).append(product)
        else:
            direct_products_by_brand.setdefault(product.brand_id, []).append(product)

    for product_list in products_by_category.values():
        product_list.sort(key=lambda item: (item.place or 0, item.name or ''))
    for product_list in direct_products_by_brand.values():
        product_list.sort(key=lambda item: (item.place or 0, item.name or ''))

    for brand in brands:
        nodes.append(
            _node(
                brand.name or '',
                brand.get_absolute_url(),
                2,
            )
        )

        for category in root_categories_by_brand.get(brand.id, []):
            _append_category_branch(
                nodes,
                category,
                depth=3,
                children_by_parent=children_by_parent,
                products_by_category=products_by_category,
            )

        for product in direct_products_by_brand.get(brand.id, []):
            nodes.append(
                _node(
                    product.name or '',
                    product.get_absolute_url(),
                    3,
                )
            )

    nodes.append(
        SitemapNode(
            title='РУ и Сертификаты',
            url=reverse('brands_with_certificates'),
            depth=1,
        )
    )

    certificate_brand_ids = _brand_certificate_ids()
    for brand in brands:
        if brand.id not in certificate_brand_ids:
            continue
        nodes.append(
            _node(
                brand.name or '',
                reverse('brand_certificates', kwargs={'pk': brand.pk}),
                2,
            )
        )

    nodes.extend(
        [
            SitemapNode(title='Контакты', url=reverse('contacts'), depth=1),
            SitemapNode(title='Политика конфиденциальности', url=reverse('privacy'), depth=1),
        ]
    )

    return _annotate_has_children(nodes)
